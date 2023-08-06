#!/usr/bin/env python3

"""
Module with a class intended to show information about any fast.
"""
import datetime

import keyboard
from vkostyanetsky import cliutils  # type: ignore

from fastimer import view


class FastsBrowser:
    """
    Class intended to show a fast's information.
    """

    _fasts: list[dict[str, datetime.datetime | int]] = []

    _max_index: int = 0
    _index: int = 0

    _prev_fast_hotkey: str = "A"
    _next_fast_hotkey: str = "D"
    _exit_hotkey: str = "Esc"

    def __init__(self, fasts: list[dict[str, datetime.datetime | int]]):
        self._fasts = fasts

        self._max_index = len(fasts) - 1
        self._index = self._max_index

    def open(self) -> None:
        """
        Starts the browser.
        """

        self.show_fast_by_index()

        keyboard.add_hotkey(self._prev_fast_hotkey, self.show_previous_fast)
        keyboard.add_hotkey(self._next_fast_hotkey, self.show_next_fast)

        keyboard.wait(self._exit_hotkey)

        keyboard.remove_all_hotkeys()

    def show_fast_by_index(self) -> None:
        """
        Draws a fast by a journal position given.
        """

        cliutils.clear_terminal()

        fast = self._fasts[self._index]
        info = view.get(fast, include_zones=True)

        for line in info:
            print(line)

        print()
        print(
            f"Press [{self._prev_fast_hotkey}] and "
            f"[{self._next_fast_hotkey}] to switch fasts."
        )
        print(f"Press [{self._exit_hotkey}] to return to the main menu.")

    def show_previous_fast(self) -> None:
        """
        Draws an information about the previous fast.
        """

        if self._index > 0:
            self._index -= 1
            self.show_fast_by_index()

    def show_next_fast(self) -> None:
        """
        Draws an information about the next fast.
        """

        if self._index < self._max_index:
            self._index += 1
            self.show_fast_by_index()
