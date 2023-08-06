from sys import argv, exit
import signal

from pyntcli import __version__ as cli_version
from pyntcli.commands import pynt_cmd
from pyntcli.pynt_docker import pynt_container
from pyntcli.ui import ui_thread
from pyntcli.auth import login 

def signal_handler(signal_number, frame):
    pynt_container.PyntContainerRegistery.instance().stop_all_containers() 
    ui_thread.stop()
    exit(0)

import requests
from distutils.version import StrictVersion
VERSION_CHECK_URL = "https://pypi.org/pypi/pyntcli/json"

def check_is_latest_version(current_version):
    res = requests.get(VERSION_CHECK_URL) 
    res.raise_for_status()
    
    avail_versions = list(res.json()["releases"].keys())
    avail_versions.sort(key=StrictVersion)

    if current_version != avail_versions[-1]:
        ui_thread.print(ui_thread.PrinterText("""
Pynt CLI new version is available, upgrade now with:
pip3 install --upgrade pyntcli
""",ui_thread.PrinterText.WARNING))

def check_for_dependecies():
    pynt_container.get_docker_type()

def print_header():
    ui_thread.print(ui_thread.PrinterText(*ui_thread.pynt_header()) \
                             .with_line(*ui_thread.pynt_version()) \
                             .with_line(""))
def main():
    print_header()
    try:
        check_for_dependecies()
        check_is_latest_version(cli_version)
        signal.signal(signal.SIGINT, signal_handler)
        cli = pynt_cmd.PyntCommand()
        cli.run_cmd(cli.parse_args(argv[1:]))
    except pynt_cmd.PyntCommandException:
       pynt_cmd.root.usage()
    except pynt_container.DockerNotAvailableException:
        ui_thread.print(ui_thread.PrinterText("Docker was unavailable, please make sure docker is installed and running.", ui_thread.PrinterText.WARNING))
    except requests.exceptions.SSLError: 
        ui_thread.print(ui_thread.PrinterText("We encountered SSL issues and could not proceed, this may be the cause of a VPN or a Firewall in place.", ui_thread.PrinterText.WARNING))
    except login.Timeout: 
        ui_thread.print(ui_thread.PrinterText("Pynt CLI exited due to incomplete registration, please try again.", ui_thread.PrinterText.WARNING))
    finally:
        ui_thread.stop()

if __name__ == "__main__":
    main()
