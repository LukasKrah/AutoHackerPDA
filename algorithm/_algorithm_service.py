"""
algorithm/_algorithm_service.py

Project: AutoHackerPDA
Created: 19.04.2023
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

import numpy as np
from typing import Literal
from copy import deepcopy


##################################################
#                     Code                       #
##################################################

PADS: Literal["oneway_up", "oneway_right",
              "corner_top_right", "corner_right_bot", "corner_bot_left", "corner_left_top",
              "junction_top", "junction_bot", "junction_left", "junction_right"]


class _Pad:
    __model: Literal["oneway", "corner", "junction", ""]
    __facing: Literal["top", "right", "bot", "left", ""]
    __state: bool

    __DIRECTIONS: list[Literal["top", "left", "bot", "right"]] = ["top", "left", "bot", "right"]

    __port_top: bool
    __port_bot: bool
    __port_right: bool
    __port_left: bool

    def __init__(self):
        self.__model = ""
        self.__facing = ""
        self.__state = False

        self.__port_top = False
        self.__port_bot = False
        self.__port_right = False
        self.__port_left = False

    def __update(self) -> None:
        # Facing: Top -> top, left, bot, right
        emitting: tuple[bool, bool, bool, bool] = (False,) * 4

        if self.__model == "oneway":
            emitting = (True, False, True, False)
        elif self.__model == "corner":
            emitting = (True, False, False, True)
        elif self.__model == "junction":
            emitting = (True, True, False, True)

        if self.__facing != "":
            self.__port_top = emitting[(0-self.__DIRECTIONS.index(self.__facing)) % 4]
            self.__port_left = emitting[(1-self.__DIRECTIONS.index(self.__facing)) % 4]
            self.__port_bot = emitting[(2-self.__DIRECTIONS.index(self.__facing)) % 4]
            self.__port_right = emitting[(3-self.__DIRECTIONS.index(self.__facing)) % 4]

    def __repr__(self) -> str:
        return f"Model: {self.__model} - Facing: {self.__facing} - Ports(T, L, B, R): " \
               f"{self.__port_top}, {self.__port_left}, {self.__port_bot}, {self.__port_right}"

    def set_attributes(self, pad_string: str) -> None:
        cut_string: list[Literal["oneway", "corner", "junction", "", "top", "bot", "left", "right"]]
        cut_string = pad_string.split("_") # noqa

        if len(cut_string) >= 2:
            self.__model = cut_string[0]
            self.__facing = cut_string[1]
        else:
            self.__model = ""
            self.__facing = ""
        self.__update()

    def rotate_by(
            self,
            by: int | None = 1
    ) -> None:
        if self.__facing != "":
            self.__facing = self.__DIRECTIONS[(self.__DIRECTIONS.index(self.__facing) + by) % 4]
            self.__update()

    @property
    def state(self) -> bool:
        return self.__state

    @state.setter
    def state(self, value: bool) -> None:
        self.__state = value

    def empower(self, direction: Literal["top", "left", "bot", "right"]) -> None:
        self.__state = self.__dict__[f"_Pad__port_{direction}"]
        self.__update()

    @property
    def port_top(self) -> bool:
        return self.__port_top

    @property
    def port_left(self) -> bool:
        return self.__port_left

    @property
    def port_bot(self) -> bool:
        return self.__port_bot

    @property
    def port_right(self) -> bool:
        return self.__port_right

    @property
    def facing(self) -> Literal["top", "left", "bot", "right"]:
        return self.__facing

    @facing.setter
    def facing(self, value: Literal["top", "left", "bot", "right"]) -> None:
        self.__facing = value
        self.__update()

    @property
    def model(self) -> Literal["oneway", "corner", "junction", ""]:
        return self.__model


class _Simulation:
    # rows[columns[]]
    __pads: list[list[_Pad]]
    __io_ports: tuple[int, int]
    __img_directions: list[list[Literal["top", "left", "bot", "right"]]]
    __initial_directions: list[list[Literal["top", "left", "bot", "right"]]]

    __found: bool
    __found_history: list[tuple[int, int]]
    __found_directions: list[list[Literal["top", "left", "bot", "right"]]]

    __histories: list[list[tuple[int, int]]]

    __DIRECTIONS: list[Literal["top", "left", "bot", "right"]] = ["top", "left", "bot", "right"]

    def __init__(self):
        self.__pads = []
        self.__io_ports = (0, 0)
        self.__init_directions = []
        self.__img_directions = []

        self.__histories = []

        self.__found = False
        self.__found_history = []
        self.__found_directions = []

        for x in range(8):
            row_list: list[_Pad] = []

            for y in range(8):
                row_list.append(_Pad())

            self.__pads.append(row_list)

    def update_pads(self, pad_strings: list[list[str]]) -> None:
        for x in range(8):
            for y in range(8):
                self.__pads[x][y].set_attributes(pad_strings[x][y])

    def update_io_ports(self, io_ports: tuple[int, int]) -> None:
        self.__io_ports = io_ports

    def set_initial_directions(self) -> None:
        self.__init_directions = self.get_directions(False)

    def simulate(self) -> list[tuple[int, int]]:
        print("START SIM")
        self.__found = False
        self.__found_history = []
        self.__found_directions = []
        self.__histories = []

        row: int = self.__io_ports[0]
        col: int = 0

        pad: _Pad = self.__pads[row][col]

        self.set_initial_directions()

        pad.empower("left")
        while not pad.state:
            pad.rotate_by()
            pad.empower("left")

        self.algorithm_basic(row, col, self.get_directions(False), "left", [])
        print("END SIM")
        return self.__found_history

    def algorithm_basic(
            self,
            row: int,
            col: int,
            pad_turns: list[list[Literal["top", "left", "bot", "right"]]],
            input_direction: Literal["top", "left", "bot", "right"] | None = "left",
            history2: list[tuple[int, int]] | None = None,
    ) -> None:
        # Deecopy lists to not influnce outer lists
        pad_turns = deepcopy(pad_turns)
        history = deepcopy(history2)

        # Set pad instances to wanted directions
        for r, pad_row in enumerate(self.__pads):
            for c, pad in enumerate(pad_row):
                pad.facing = pad_turns[r][c]

        # Add self to history
        history.append((row, col))

        pad: _Pad = self.__pads[row][col]

        if history in self.__histories:
            return
        self.__histories.append(history)

        for direction in range(4):
            if self.__found:
                return

            # Rest state, rotate and evaluate state
            pad.state = False
            if direction != 0:
                pad.rotate_by(1)
            pad.empower(input_direction)

            pad_turns[row][col] = pad.facing

            # Check if pda is solved
            if row == self.__io_ports[1] and col == len(self.__pads[0]) - 1:
                if pad.port_right and pad.state:
                    self.__found = True
                    self.__found_history = history
                    self.__found_directions = pad_turns
                    return

            # Determine influenced neighbors
            influenced_neighbors: list[tuple[int, int, Literal["top", "left", "bot", "right"]]] = []

            if pad.port_top and pad.state and row != 0 and input_direction != "top":
                influenced_neighbors.append((row - 1, col, "bot"))
            if pad.port_left and pad.state and col != 0 and input_direction != "left":
                influenced_neighbors.append((row, col - 1, "right"))
            if pad.port_bot and pad.state and row != len(self.__pads) - 1 and input_direction != "bot":
                influenced_neighbors.append((row + 1, col, "top"))
            if pad.port_right and pad.state and col != len(self.__pads[0]) - 1 and input_direction != "right":
                influenced_neighbors.append((row, col + 1, "left"))

            # Resume with every influenced neighbor
            for n_row, n_col, n_input in influenced_neighbors:
                # Cancel if neighbor is already in path
                if (n_row, n_col) in history:
                    return
                self.algorithm_basic(n_row, n_col, pad_turns, n_input, history)

    def found_diffs(self, history: list[tuple[int, int]]) -> dict[tuple[int, int], int]:
        result = {}

        # Set pad instances to initial directions
        for r, pad_row in enumerate(self.__pads):
            for c, pad in enumerate(pad_row):
                pad.facing = self.__init_directions[r][c]

        for row, pad_row in enumerate(self.__found_directions):
            for col, pad in enumerate(pad_row):
                if (row, col) in history:
                    diff: int = (self.__DIRECTIONS.index(pad)
                                 - self.__DIRECTIONS.index(self.__init_directions[row][col])) % 4
                    if diff != 0:
                        result[(row, col)] = diff
                        self.__pads[row][col].rotate_by(diff)

        return result

    def get_directions(self, with_model: bool | None = True) -> list[list[Literal["top", "left", "bot", "right"] | str]]:
        directions = []
        for row in range(8):
            row_directions = []
            for col in range(8):
                row_directions.append(f"{self.__pads[row][col].model+'_' if with_model else ''}"
                                      f"{self.__pads[row][col].facing}")
            directions.append(row_directions)
        return directions


class _AlgorithmService:
    __sim: _Simulation

    def __init__(self) -> None:
        self.__sim = _Simulation()

    def path_finder(
            self,
            _pads: list[list[np.ndarray]],
            pad_directions: list[list[str]],
            io_ports: tuple[int, int]
    ) -> dict[tuple[int, int], int]:
        self.__sim.update_pads(pad_directions)
        self.__sim.update_io_ports(io_ports)

        his = self.__sim.simulate()

        diffs = self.__sim.found_diffs(his)
        # row | column

        # Window.grid_pads(_pads, self.__sim.get_directions(), io_ports)
        return diffs


AlgorithmService = _AlgorithmService()
