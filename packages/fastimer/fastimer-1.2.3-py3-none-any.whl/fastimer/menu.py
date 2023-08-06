#!/usr/bin/env python3

"""
Generates the app's main menu.
"""
import datetime

from vkostyanetsky import cliutils  # type: ignore

from fastimer import view


class FastimerMenu(cliutils.Menu):  # type: ignore
    """
    This class represents main menu of the application.
    """

    _active_fast: dict[str, datetime.datetime | int] | None = None

    def __init__(self, active_fast: dict[str, datetime.datetime | int] | None = None):
        super().__init__()

        self._active_fast = active_fast

    def _print_menu(self) -> None:
        print(self._top_border())

        self._print_title()

        self._print_active_fast()

        self._print_choices()

        print(self._bottom_border())

    def _print_title(self) -> None:
        print(self._text_line("FASTING TIMER", 2))

        print(self._inner_border())

    def _print_choices(self) -> None:
        print(self._empty_line())

        for choice in self._get_choices_to_print():
            print(self._text_line(text=choice))

        print(self._empty_line())

    def _print_active_fast(self) -> None:
        if self._active_fast is not None:
            active_fast_preview = view.get(self._active_fast)

            print(self._empty_line())

            for text in active_fast_preview:
                print(self._text_line(text))

            print(self._empty_line())

            print(self._inner_border())

    def print(self) -> None:
        """
        Draws the menu.
        """
        print()

        self._print_menu()

        print(self._prompt, end="")
