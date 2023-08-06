#!/usr/bin/env python3

"""Implementation of methods to generate detailed view of a fast."""

import datetime
import typing

from vkostyanetsky.cliutils import title_and_value  # type: ignore

from .utils import get_time_difference, is_fast_completed, is_fast_stopped


def get(fast: dict[str, typing.Any], include_zones: bool = False) -> list[str]:
    """
    Generates a detailed view of a fast.
    """

    time = fast["stopped"] if is_fast_stopped(fast) else datetime.datetime.now()

    goal = fast["started"] + datetime.timedelta(hours=fast["length"])

    description = [
        __get_fast_title(fast),
        "",
        __get_fast_from(fast),
        __get_fast_goal(fast, goal),
        "",
    ]

    if include_zones:
        __include_fasting_zones(description, fast, time)
        description.append("")

    description.append(__get_fast_progress_bar(fast, goal, time))

    description.append("")

    description.append(__get_fast_elapsed_time(fast, time))

    if time <= goal:
        description.append(__get_fast_remaining_time(time, goal))
    else:
        description.append(__get_fast_extra_time(time, goal))

    return description


def __get_fast_title(fast: dict[str, typing.Any]) -> str:
    if is_fast_stopped(fast):
        title = "COMPLETED FAST" if is_fast_completed(fast) else "FAILED FAST"
    else:
        title = "ACTIVE FAST"

    return title


def __get_fast_from(fast: dict[str, typing.Any]) -> str:
    value = __get_day(fast["started"])
    value = title_and_value("From", value, 5)

    return str(value)


def __get_fast_goal(fast: dict[str, typing.Any], goal: datetime.datetime) -> str:
    length = fast["length"]
    goal_string = __get_day(goal)
    goal_string = f"{goal_string} ({length} hours)"
    goal_string = title_and_value("Goal", goal_string, 5)

    return str(goal_string)


def __get_fast_elapsed_time(
    fast: dict[str, typing.Any], time: datetime.datetime
) -> str:
    date1 = fast["started"]
    date2 = time if fast.get("stopped") is None else fast["stopped"]

    value = __get_time_difference(date1, date2)
    value = title_and_value("Elapsed time", value, 15)

    return str(value)


def __get_fast_extra_time(time: datetime.datetime, goal: datetime.datetime) -> str:
    value = __get_time_difference(goal, time) if time >= goal else None
    value = title_and_value("Extra time", value, 15)

    return str(value)


def __get_fast_remaining_time(time: datetime.datetime, goal: datetime.datetime) -> str:
    value = (
        __get_time_difference(time - datetime.timedelta(minutes=1), goal)
        if time < goal
        else None
    )

    value = title_and_value("Remaining", value, 15)

    return str(value)


def __line_for_zone(
    note: str,
    time: datetime.datetime,
    title: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime | None,
) -> str:
    zone_from = f"from {__get_day(start_time)}"

    if end_time is None:
        zone_note = note if start_time <= time else ""
    else:
        zone_note = note if start_time <= time < end_time else ""

    zone_note = title_and_value(f"- {title}", f"{zone_from}{zone_note}")

    return str(zone_note)


def __include_fasting_zones(
    lines: list[str], fast: dict[str, typing.Any], time: datetime.datetime
) -> None:
    note = " <-- you were here" if is_fast_stopped(fast) else " <-- you are here"

    anabolic_zone = fast["started"]
    catabolic_zone = anabolic_zone + datetime.timedelta(hours=4)
    fat_burning_zone = catabolic_zone + datetime.timedelta(hours=12)
    ketosis_zone = fat_burning_zone + datetime.timedelta(hours=8)
    deep_ketosis_zone = ketosis_zone + datetime.timedelta(hours=48)

    lines.append("Fasting zones:")
    lines.append("")

    line = __line_for_zone(note, time, "Anabolic", anabolic_zone, catabolic_zone)
    lines.append(line)

    line = __line_for_zone(note, time, "Catabolic", catabolic_zone, fat_burning_zone)
    lines.append(line)

    line = __line_for_zone(note, time, "Fat burning", fat_burning_zone, ketosis_zone)
    lines.append(line)

    line = __line_for_zone(note, time, "Ketosis", ketosis_zone, deep_ketosis_zone)
    lines.append(line)

    line = __line_for_zone(note, time, "Anabolic", deep_ketosis_zone, None)
    lines.append(line)


def __get_fast_progress_bar(
    fast: dict[str, typing.Any], goal: datetime.datetime, time: datetime.datetime
) -> str:
    seconds_now = (time - fast["started"]).total_seconds()
    seconds_all = (goal - fast["started"]).total_seconds()

    percent = round(seconds_now / seconds_all * 100, 1)

    done_len = int(percent // 2.5)
    done_len = min(done_len, 40)

    left_len = int(40 - done_len)

    left = "-" * left_len
    done = "#" * done_len
    tail = str(percent)

    return f"{done}{left} {tail}%"


def __get_time_difference(
    start_date: datetime.datetime, end_date: datetime.datetime
) -> str:
    hours, minutes = get_time_difference(start_date, end_date)

    hours_string = str(hours).zfill(2)
    minutes_string = str(minutes).zfill(2)

    return f"{hours_string}h {minutes_string}m"


def __get_day(date: datetime.datetime) -> str:
    if (datetime.datetime.now() - date).days > 7:
        fmt = "%Y-%m-%d %H:%M"
    else:
        fmt = "%a, %H:%M"

    return date.strftime(fmt)
