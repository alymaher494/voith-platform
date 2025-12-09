"""
Utility functions for the video downloader.

This module contains helper functions for time parsing and validation,
used throughout the downloader system for handling time-based operations
like video slicing.
"""
from typing import Optional


def parse_time(time_str: Optional[str]) -> Optional[int]:
    """
    Parse a time string into total seconds.

    Supports both mm:ss and hh:mm:ss formats. Returns None if input is None.

    Args:
        time_str (Optional[str]): Time string in format "mm:ss" or "hh:mm:ss",
                                 or None to return None

    Returns:
        Optional[int]: Total seconds from the time string, or None if input was None

    Raises:
        ValueError: If the time string format is invalid

    Examples:
        >>> parse_time("1:30")
        90
        >>> parse_time("01:30:45")
        5445
        >>> parse_time(None)
        None
    """
    if time_str is None:
        return None

    parts = time_str.split(':')
    try:
        if len(parts) == 2:
            # mm:ss format
            minutes, seconds = map(int, parts)
            if minutes < 0 or seconds < 0 or seconds >= 60:
                raise ValueError
            return minutes * 60 + seconds
        elif len(parts) == 3:
            # hh:mm:ss format
            hours, minutes, seconds = map(int, parts)
            if hours < 0 or minutes < 0 or minutes >= 60 or seconds < 0 or seconds >= 60:
                raise ValueError
            return hours * 3600 + minutes * 60 + seconds
        else:
            raise ValueError
    except ValueError:
        raise ValueError(f"Invalid time format: '{time_str}'. Use 'mm:ss' or 'hh:mm:ss'")


def validate_time_range(start_time: Optional[int], end_time: Optional[int]) -> bool:
    """
    Validate that start time is before end time for video slicing.

    Both times must be provided and start_time must be less than end_time.

    Args:
        start_time (Optional[int]): Start time in seconds, or None
        end_time (Optional[int]): End time in seconds, or None

    Returns:
        bool: True if validation passes

    Raises:
        ValueError: If times are invalid or start_time >= end_time

    Examples:
        >>> validate_time_range(30, 90)
        True
        >>> validate_time_range(90, 30)
        ValueError: Start time (90s) must be less than end time (30s)
    """
    if start_time is None or end_time is None:
        return True  # Allow None values (no slicing)

    if start_time < 0 or end_time < 0:
        raise ValueError("Time values cannot be negative")

    if start_time >= end_time:
        raise ValueError(f"Start time ({start_time}s) must be less than end time ({end_time}s)")

    return True
