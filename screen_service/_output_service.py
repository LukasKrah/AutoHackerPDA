"""
screen_service/_output_service.py

Project: AutoHackerPDA
Created: 18.04.2023
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from time import sleep
import pyautogui
import autoit


##################################################
#                     Code                       #
##################################################

class OutputService:
    """
    Do something one the screen
    """

    @classmethod
    def pad_clicks(cls, click: dict[tuple[int, int], int]) -> None:
        width: int
        height: int
        width, height = pyautogui.size()

        x_left: int = (width // 3) + 40
        x_right: int = int(width / 1.536) - 30
        y_top: int = int(height / 3.85714)
        y_bot: int = int(height / 1.30120)

        field_width = (x_right - x_left) // 8
        field_height = (y_bot - y_top) // 8

        for row, col in click:
            x: int = x_left + (field_width * col) + (field_width // 2)
            y: int = y_top + (field_height * row) + (field_height // 2)
            for i in range(click[(row, col)]):
                autoit.mouse_click("left", x, y, speed=0)
                sleep(0.02)
