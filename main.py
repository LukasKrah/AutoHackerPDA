"""
/main.py

Project: NextLevelHackerPDA
Created: 18.04.2023
Author: Lukas Krahbichler
"""

from pynput import keyboard
from screen_service import InputService, Window
from algorithm import AlgorithmService
from ai_analyze import CompareService


def on_press(key):
    ...


def on_release(key):
    if str(key) == "'o'":
        pads = InputService.pda_single()
        io_pads = InputService.pda_io()

        styles = CompareService.compare_pads(pads)
        io = CompareService.compare_io(io_pads)
        print(io)
        clicks = AlgorithmService.path_finder(pads, styles, io)

        InputService.pad_clicks(clicks)


if __name__ == '__main__':

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
