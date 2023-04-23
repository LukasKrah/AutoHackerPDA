"""
cv_analyze/_compare.py

Project: AutoHackerPDA
Created: 18.04.2023
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from typing import Literal
import numpy as np
import cv2


##################################################
#                     Code                       #
##################################################

PADS: Literal["oneway_top", "oneway_right",
              "corner_top_right", "corner_right_bot", "corner_bot_left", "corner_left_top",
              "junction_top", "junction_bot", "junction_left", "junction_right"]


class _CompareService:
    THRESHOLD: float = 0.80

    def compare_io(self, pads: list[list[np.ndarray]]) -> tuple[int, int]:
        imgs = ["arrows_in.png", "arrows_out.png"]

        compared = self.compare_pads(pads, imgs=imgs, threshold=0.5)
        res = []

        for in_out in compared:
            for i, comp in enumerate(in_out):
                if comp != "":
                    res.append(i)
                    break
            else:
                res.append(0)

        return res[0], res[1]

    def compare_pads(
            self,
            pads: list[list[np.ndarray]],
            imgs: list[str] | None = None,
            threshold: float | None = None
    ) -> list[list[str]]:
        results: list[list[str]] = []

        if not threshold:
            threshold = self.THRESHOLD

        if not imgs:
            imgs = ["oneway_top.png", "oneway_right.png",
                    "corner_top_right.png", "corner_right_bot.png",
                    "corner_bot_left.png", "corner_left_top.png",
                    "junction_top.png", "junction_bot.png",
                    "junction_left.png", "junction_right.png"]

        imgs_to_compare: list[tuple[np.ndarray, PADS]] = []

        for img in imgs:
            imgs_to_compare.append((
                cv2.cvtColor(cv2.imread("imgs/"+img), cv2.COLOR_BGR2GRAY),
                "".join(img.split(".")[:-1])
            ))

        for pad_col in pads:
            col_list: list[str] = []

            for pad_row in pad_col:
                for img_to_compare in imgs_to_compare:
                    res = cv2.matchTemplate(pad_row, img_to_compare[0], cv2.TM_CCOEFF_NORMED)

                    loc = np.where(res >= threshold)
                    loc_list = [*zip(*loc[::-1])]
                    if loc_list:
                        col_list.append(img_to_compare[1])
                        break
                else:
                    col_list.append("")

            results.append(col_list)

        return results


CompareService = _CompareService()
