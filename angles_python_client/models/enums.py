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


class ExecutionTypes(str, Enum):
    """Whether a build or execution came from an automated framework or a manual test run.

    Read-only from this client's point of view. The value is assigned by the Angles
    server - a reporting client setting it to MANUAL would put a build on the dashboard
    that no manual test run exists to explain - so it is absent from CreateBuild and
    CreateExecution and only ever used to read results back or to filter a list call.
    """

    AUTOMATED = "automated"
    MANUAL = "manual"


class GroupingPeriods(str, Enum):
    DAY = "day"
    WEEK = "week"
    FORTNIGHT = "fortnight"
    MONTH = "month"
    YEAR = "year"
