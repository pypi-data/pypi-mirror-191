import argparse
from copy import deepcopy
import os
import webbrowser
from http import HTTPStatus
import requests
import time
from subprocess import Popen, PIPE

from pyntcli.store.store import CredStore
from pyntcli.pynt_docker import pynt_container
from pyntcli.ui import ui_thread
from . import sub_command

def proxy_usage():
    return ui_thread.PrinterText("Command integration to Pynt. Run a security scan with a given command.") \
        .with_line("") \
        .with_line("Usage:",style=ui_thread.PrinterText.HEADER) \
        .with_line("\tpynt command [OPTIONS]") \
        .with_line("") \
        .with_line("Options:",style=ui_thread.PrinterText.HEADER) \
        .with_line("\t--cmd - The command that runs the functional tests") \
        .with_line("\t--port - set the port pynt will listen to (DEFAULT: 5001)") \
        .with_line("\t--proxy-port - set the port proxied traffic should be routed to (DEFAULT: 6666)") \
        .with_line("\t--insecure - use when target uses self signed certificates")


class ProxyCommand(sub_command.PyntSubCommand): 
    def __init__(self, name) -> None:
        super().__init__(name)
        self.scan_id = ""
        self.proxy_sleep_interval = 2
        self.proxy_healthcheck_buffer = 10
        self.proxy_server_base_url = "http://localhost:{}/api"
    
    def print_usage(self, *args):
        ui_thread.print(proxy_usage())

    def add_cmd(self, parent: argparse._SubParsersAction) -> argparse.ArgumentParser:
        proxy_cmd = parent.add_parser(self.name)
        proxy_cmd.add_argument("--port", "-p", help="", type=int, default=5001)
        proxy_cmd.add_argument("--proxy-port", help="", type=int, default=6666) 
        proxy_cmd.add_argument("--cmd", help="", default="", required=True)
        proxy_cmd.print_usage = self.print_usage
        proxy_cmd.print_help = self.print_usage
        return proxy_cmd
    
    def _updated_environment(self, args):
        env_copy = deepcopy(os.environ)
        return env_copy.update({"HTTP_PROXY": "http://localhost:{}".format(args.proxy_port)})
    
    def _start_proxy(self, args):
        res = requests.put(self.proxy_server_base_url.format(args.port) + "/proxy/start")
        res.raise_for_status()
        self.scan_id = res.json()["scanId"]
    
    def _stop_proxy(self, args):
        start = time.time()
        while start + self.proxy_healthcheck_buffer > time.time(): 
            res = requests.put(self.proxy_server_base_url.format(args.port) + "/proxy/stop", json={"scanId": self.scan_id})
            if res.status_code == HTTPStatus.OK: 
                return 
            time.sleep(self.proxy_sleep_interval)
        raise TimeoutError()
        
    def _get_report(self, args):
        while True: 
            res = requests.get(self.proxy_server_base_url.format(args.port) + "/report", params={"scanId": self.scan_id})
            ui_thread.print("status code is: {}".format(res.status_code))
            if res.status_code == HTTPStatus.OK:
                return res.text
            if res.status_code == HTTPStatus.ACCEPTED:
                time.sleep(self.proxy_sleep_interval)
                continue
            ui_thread.print("Error in polling for scan report: {}".format(res.text))
            return 
    
    def _healthcheck(self, args):
        start = time.time()
        while start + self.proxy_healthcheck_buffer > time.time(): 
            try:
                res = requests.get(self.proxy_server_base_url.format(args.port) + "/healthcheck")
                if res.status_code == 418:
                    return 
            except: 
                time.sleep(self.proxy_sleep_interval)
        raise TimeoutError()

    def run_cmd(self, args: argparse.Namespace):
        docker_type, docker_arguments = pynt_container.get_container_with_arguments(pynt_container.PyntDockerPort("5001", args.port, "--port"), 
                                                    pynt_container.PyntDockerPort("6666", args.proxy_port, "--proxy-port"))
        
        if "insecure" in args and args.insecure:
            docker_arguments.append("--insecure")

        if "dev_flags" in args:
            docker_arguments += args.dev_flags.split(" ")
        
        creds_path = CredStore().get_path()

        proxy_docker = pynt_container.PyntContainer(image_name=pynt_container.PYNT_DOCKER_IMAGE, 
                                    tag="proxy-latest", 
                                    mounts=[pynt_container.create_mount(creds_path, "/app/creds.json")],
                                    detach=True, 
                                    args=docker_arguments)
        proxy_docker.run(docker_type)
        ui_thread.print_generator(proxy_docker.stdout)
        self._healthcheck(args)

        self._start_proxy(args) 

        user_process = Popen(args.cmd, shell=True, stdout=PIPE, stderr=PIPE, env=self._updated_environment(args))
        ui_thread.print_generator(user_process.stdout)
        ui_thread.print_generator(user_process.stderr)
        user_process.wait()

        self._stop_proxy(args)

        report = self._get_report(args)
        with open("report.html", "w") as f:
            f.write(report)
        webbrowser.open("file://{}/report.html".format(os.getcwd()))
