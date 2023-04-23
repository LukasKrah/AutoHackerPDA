"""
screen_service/_visualization.py

Project: AutoHackerPDA
Created: 18.04.2023
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from tkinter import Tk, Canvas
from PIL import Image, ImageTk
from typing import Any
import numpy as np


##################################################
#                     Code                       #
##################################################

class _Window(Tk):
    __imgs: list[ImageTk.PhotoImage]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.__imgs = []

    def grid_pads(self, images: list[list[np.ndarray]], pad_styles: list[list[str]] | None = None,
                  io_ports: tuple[int, int] | None = None) -> None:
        for slave in self.grid_slaves():
            slave.grid_forget()
            slave.destroy()
        self.__imgs = []

        for row, image_row in enumerate(images):
            for col, image_col in enumerate(image_row):
                self.__imgs.append(ImageTk.PhotoImage(image=Image.fromarray(image_col)))
                can = Canvas(self)
                width = self.__imgs[-1].width()
                height = self.__imgs[-1].height()

                can.configure(width=width, height=height)

                can.create_image(0, 0, anchor="nw", image=self.__imgs[-1])

                if pad_styles:
                    if pad_styles[row][col] in "oneway_toponeway_bot":
                        can.create_line(width//2, 0, width//2, height, fill="red", width=5)
                    elif pad_styles[row][col] in "oneway_rightoneway_left":
                        can.create_line(0, height//2, width, height//2, fill="red", width=5)
                    elif pad_styles[row][col] in "corner_top_right":
                        can.create_line(width//2, 0, width//2, height//2, fill="red", width=5)
                        can.create_line(width//2, height//2, width, height//2, fill="red", width=5)
                    elif pad_styles[row][col] in "corner_right_bot":
                        can.create_line(width//2, height//2, width, height//2, fill="red", width=5)
                        can.create_line(width//2, height//2, width//2, height, fill="red", width=5)
                    elif pad_styles[row][col] in "corner_bot_left":
                        can.create_line(width//2, height//2, width//2, height, fill="red", width=5)
                        can.create_line(0, height//2, width//2, height//2, fill="red", width=5)
                    elif pad_styles[row][col] in "corner_left_top":
                        can.create_line(0, height//2, width//2, height//2, fill="red", width=5)
                        can.create_line(width//2, 0, width//2, height//2, fill="red", width=5)
                    elif pad_styles[row][col] in "junction_top":
                        can.create_line(0, height//2, width, height//2, fill="red", width=5)
                        can.create_line(width//2, 0, width//2, height//2, fill="red", width=5)
                    elif pad_styles[row][col] in "junction_bot":
                        can.create_line(0, height//2, width, height//2, fill="red", width=5)
                        can.create_line(width//2, height//2, width//2, height, fill="red", width=5)
                    elif pad_styles[row][col] in "junction_right":
                        can.create_line(width//2, 0, width//2, height, fill="red", width=5)
                        can.create_line(width//2, height//2, width, height//2, fill="red", width=5)
                    elif pad_styles[row][col] in "junction_left":
                        can.create_line(width//2, 0, width//2, height, fill="red", width=5)
                        can.create_line(0, height//2, width//2, height//2, fill="red", width=5)

                if io_ports:
                    if col == 0 and row == io_ports[0]:
                        can.create_line(0, 0, 0, height, fill="green", width=15)

                    if col == len(image_row)-1 and row == io_ports[1]:
                        can.create_line(width, 0, width, height, fill="blue", width=15)
                can.grid(row=row, column=col, sticky="NSEW")

        self.grid_rowconfigure("all", weight=1)
        self.grid_columnconfigure("all", weight=1)


Window = _Window()
