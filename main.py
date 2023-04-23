"""
/main.py

Project: AutoHackerPDA
Created: 18.04.2023
Author: Lukas Krahbichler
"""

from concurrent.futures import ThreadPoolExecutor
from os import kill, getpid
from time import sleep
import keyboard

from screen_service import InputService, OutputService
from algorithm import AlgorithmService
from cv_analyze import CompareService


def start():
    pads = InputService.pda_single()
    io_pads = InputService.pda_io()

    styles = CompareService.compare_pads(pads)
    io = CompareService.compare_io(io_pads)
    clicks = AlgorithmService.path_finder(pads, styles, io)

    OutputService.pad_clicks(clicks)


def test():
    import autoit

    def inner_function():
        sleep(2)
        while True:
            autoit.mouse_click("left", speed=0)
            sleep(0.1)
            start()
            sleep(3)

    tp = ThreadPoolExecutor(max_workers=1)
    tp.submit(inner_function)


if __name__ == '__main__':
    keyboard.add_hotkey("ctrl+x", start)
    keyboard.add_hotkey("ctrl+v", test)
    keyboard.add_hotkey("ctrl+c", lambda: kill(getpid(), 9))

    keyboard.wait()
