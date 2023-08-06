from threading import Thread
import queue
import os
from rich.text import Text
from rich.console import Console
from typing import Tuple

from pyntcli import __version__ as cli_version

class PrinterText():
    DEFAULT = 0
    HEADER = 1
    INFO = 2
    WARNING = 3

    def __init__(self,text,style=DEFAULT):
        self.text = Text(text, PrinterText.get_style(style))

    @staticmethod
    def get_style(style):
        if style == PrinterText.INFO:
            return "bold blue"
        if style == PrinterText.WARNING:
            return "bold red"
        if style == PrinterText.HEADER:
            return "bold"
        if style == PrinterText.DEFAULT:
            return None

    def with_line(self, line, style=DEFAULT):
        self.text.append(os.linesep)
        self.text.append(Text(line, PrinterText.get_style(style)))
        return self

def pynt_version()-> Tuple[str,int]: 
    return "Pynt CLI version " + cli_version,PrinterText.DEFAULT

def pynt_header()-> Tuple[str,int]:
    return "API Security testing autopilot",PrinterText.DEFAULT

def gen_func_loop(gen):
    for l in gen:
        data = l
        if type(data) == bytes: 
            data = l.decode("utf-8")
        if data[-1] == "\n":
            data = data[:-1]
        _print(data)
        
def print_generator(gen):
    t = Thread(target=gen_func_loop, args=(gen,), daemon=True) 
    t.start()

def _print(s): 
    Printer.instance().print(s)

def print(s): 
    if type(s) == bytes: 
        s = s.decode("utf-8")
    _print(s)

def stop():
    Printer.instance().stop()

class Printer():
    _instace = None

    def __init__(self) -> None:
        self.running = False
        self.run_thread = Thread(target=self._print_in_loop, daemon=True)
        self.print_queue = queue.Queue()
        self.console = Console(tab_size=4)
   
    @staticmethod 
    def instance():
        if not Printer._instace:
            Printer._instace = Printer() 
            Printer._instace.start() 

        return Printer._instace

    def start(self):
        self.running = True
        self.run_thread.start()
    
    def _print_in_loop(self):
        while self.running:
            try: 
                self.console.print(self.print_queue.get(timeout=1))
            except queue.Empty:
                pass
        
        while not self.print_queue.empty():
            self.console.print(self.print_queue.get())


    def print(self, data):
        if isinstance(data,PrinterText):
            data = data.text
        self.print_queue.put(data)
    
    def stop(self):
        self.running = False
        self.run_thread.join()

