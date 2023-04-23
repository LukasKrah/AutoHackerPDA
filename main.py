"""
/main.py

Project: AutoHackerPDA
Created: 18.04.2023
Author: Lukas Krahbichler
"""

from concurrent.futures import ThreadPoolExecutor
from pynput import keyboard
from os import kill, getpid
from time import sleep

from screen_service import InputService, OutputService
from algorithm import AlgorithmService
from cv_analyze import CompareService


def on_press(_key):
    ...


def on_release(key):
    if str(key) == "'o'":
        pads = InputService.pda_single()
        io_pads = InputService.pda_io()

        styles = CompareService.compare_pads(pads)
        io = CompareService.compare_io(io_pads)
        clicks = AlgorithmService.path_finder(pads, styles, io)

        OutputService.pad_clicks(clicks)

    elif str(key) == "'c'":
        kill(getpid(), 9)


def key_input():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def test():
    import autoit

    sleep(2)
    while True:
        autoit.mouse_click("left", speed=0)
        sleep(0.1)
        on_release("'o'")
        sleep(3)


if __name__ == '__main__':
    tp = ThreadPoolExecutor(max_workers=1)
    tp.submit(key_input)
