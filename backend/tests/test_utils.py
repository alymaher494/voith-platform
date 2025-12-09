"""
Tests for utility functions.
"""
import pytest
from src.downloader.utils import parse_time, validate_time_range


def test_parse_time_valid():
    assert parse_time("01:30") == 90
    assert parse_time("01:02:03") == 3723


def test_parse_time_invalid():
    with pytest.raises(ValueError, match="Invalid time format"):
        parse_time("invalid")
    with pytest.raises(ValueError, match="Invalid time format"):
        parse_time("01:02:03:04")


def test_validate_time_range_valid():
    assert validate_time_range(0, 10) is True
    assert validate_time_range(5, 15) is True


def test_validate_time_range_invalid():
    with pytest.raises(ValueError,
                       match=r"Start time \(10s\) must be less than end time \(5s\)"):
        validate_time_range(10, 5)
