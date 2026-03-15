from __future__ import annotations

from enum import Enum


class ExecutionStates(str, Enum):
    SKIPPED = "SKIPPED"
    PASS = "PASS"
    ERROR = "ERROR"
    FAIL = "FAIL"


class StepStates(str, Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"
    PASS = "PASS"
    ERROR = "ERROR"
    FAIL = "FAIL"


class GroupingPeriods(str, Enum):
    DAY = "day"
    WEEK = "week"
    FORTNIGHT = "fortnight"
    MONTH = "month"
    YEAR = "year"
