#!/usr/bin/env python3

"""
Helpers widely used in the application.
"""

import datetime
import typing


def get_time_difference(
    start_date: datetime.datetime, end_date: datetime.datetime
) -> tuple[int, int]:
    """
    Return time difference between two dates as a (hours, seconds) tuple.
    """

    seconds_per_hour = 3600
    seconds_per_minute = 60

    seconds = (end_date - start_date).total_seconds()

    hours = int(seconds // seconds_per_hour)
    minutes = int(seconds % seconds_per_hour // seconds_per_minute)

    return hours, minutes


def print_with_alignment(title: str, value: str, width: int = 15) -> None:
    """
    Prints a string with an alighment given.
    """

    title = f"{title}:".ljust(width)

    print(f"{title} {value}")


def get_active_fast(
    fasts: list[dict[str, datetime.datetime | int]]
) -> dict[str, typing.Any] | None:
    """
    Return data of the active fast.
    """

    return fasts[-1] if len(fasts) > 0 and fasts[-1].get("stopped") is None else None


def is_fast_stopped(fast: dict[str, datetime.datetime | int]) -> bool:
    """
    Determines whether a fast is over or not.
    """

    return fast.get("stopped") is not None


def is_fast_completed(fast: dict[str, typing.Any]) -> bool:
    """
    Checks if a fast completed.
    """

    hours_in_fast = get_fast_length(fast)[0]
    fast_length = fast["length"] if fast["length"] is not None else 0

    return int(fast_length) <= hours_in_fast


def get_fast_length(fast: dict[str, typing.Any]) -> tuple[int, int]:
    """
    Returns length of a fast as a (hours, seconds) tuple.
    """

    started = fast["started"]
    stopped = fast.get("stopped")

    if stopped is not None:
        result = get_time_difference(started, stopped)
    else:
        result = 0, 0

    return result
