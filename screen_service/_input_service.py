"""
screen_service/_input_service.py

Project: AutoHackerPDA
Created: 18.04.2023
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

import numpy as np
import pyautogui
import cv2


##################################################
#                     Code                       #
##################################################

class InputService:
    """
    Input something from the screen
    """

    @staticmethod
    def screenshot() -> np.ndarray:
        return cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_BGR2GRAY)
        # img = cv2.imread("imgs/screen.png")
        # return np.array(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

    @classmethod
    def pda_whole(cls) -> np.ndarray:
        # 640, 280 - 1250, 830
        screen: np.ndarray = cls.screenshot()

        height: int
        width: int
        height, width = screen.shape[:2]

        x_left: int = width // 3
        x_right: int = int(width / 1.536)
        y_top: int = int(height / 3.85714)
        y_bot: int = int(height / 1.30120)

        return screen[y_top:y_bot, x_left:x_right]

    @classmethod
    def pda_io(cls) -> list[list[np.ndarray]]:
        pdas: list[list[np.ndarray]] = cls.pda_single(0, 1, 20, 8)

        return [[row[0] for row in pdas], [row[-1] for row in pdas]]

    @classmethod
    def pda_single(
            cls,
            cut_left: int | None = 40,
            cut_right: int | None = 30,
            pad_x: int | None = 8,
            pad_y: int | None = 8
    ) -> list[list[np.ndarray]]:
        pda: np.ndarray = cls.pda_whole()[:, cut_left:-cut_right]

        PAD_X: int = pad_x
        PAD_Y: int = pad_y

        pad_height: float = pda.shape[0] / PAD_Y
        pad_width: float = pda.shape[1] / PAD_X

        pdas: list[list[np.ndarray]] = []
        for y in range(PAD_Y):
            row_list: list[np.ndarray] = []
            for x in range(PAD_X):
                row_list.append(pda[int(pad_height*y):int(pad_height*(y+1)), int(pad_width*x):int(pad_width*(x+1))])

            pdas.append(row_list)

        return pdas
