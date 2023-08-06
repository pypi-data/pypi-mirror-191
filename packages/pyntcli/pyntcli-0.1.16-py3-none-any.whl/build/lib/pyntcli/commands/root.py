import argparse
import sys

from pyntcli.auth import login
from pyntcli.ui import ui_thread

def root_usage():
    return ui_thread.PrinterText(*ui_thread.pynt_header()) \
        .with_line(*ui_thread.pynt_version()) \
        .with_line("") \
        .with_line("Usage:",style=ui_thread.PrinterText.HEADER) \
        .with_line("\tpynt [COMMAND] [OPTIONS]") \
        .with_line("") \
        .with_line("Commands:",style=ui_thread.PrinterText.HEADER) \
        .with_line("\tpostman - integration with postman, run scan from pynt postman collection") \
        .with_line("\tpynt-id - view your pynt-id to use when running pynt in CI pipeline") \
        .with_line("") \
        .with_line("Run pynt [COMMAND] -h to get help on a specific command",style=ui_thread.PrinterText.INFO)

def usage(*args):
    ui_thread.print(root_usage())

class BaseCommand():
    def __init__(self) -> None:
        self.base: argparse.ArgumentParser = None
        self.subparser: argparse._SubParsersAction = None

    def cmd(self):
        if self.base:
            return self.base
        
        self.base = argparse.ArgumentParser(prog="pynt")
        self.base.print_usage = usage
        self.base.print_help = usage
        return self.base 
   
    def add_base_arguments(self, parser):
        parser.add_argument("--insecure", default=False, required=False, action='store_true',help="use when target uses self signed certificates")
        parser.add_argument("--dev-flags", type=str,default="",  help=argparse.SUPPRESS)

    def get_subparser(self) -> argparse._SubParsersAction:
        if self.subparser is None:
            self.subparser = self.base.add_subparsers(help="", dest="command")
        
        return self.subparser

    def run_cmd(self, args: argparse.Namespace):
        if login.should_login():
            l = login.Login().login()
        else:
            login.refresh_token()  
