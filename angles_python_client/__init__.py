"""angles-python-client

Public API mirrors `angles-javascript-client`:

- A singleton reporter (`angles_reporter`) similar to the JS default export.
- Request classes: BuildRequests, TeamRequests, EnvironmentRequests, ScreenshotRequests,
  ExecutionRequests, BaselineRequests, MetricRequests, AnglesRequests.
"""

from .http import AnglesHttpClient
from .reporter import AnglesReporter, angles_reporter
from .requests import (
    BuildRequests,
    TeamRequests,
    EnvironmentRequests,
    ScreenshotRequests,
    ExecutionRequests,
    BaselineRequests,
    MetricRequests,
    AnglesRequests,
)

__all__ = [
    "AnglesHttpClient",
    "AnglesReporter",
    "angles_reporter",
    "BuildRequests",
    "TeamRequests",
    "EnvironmentRequests",
    "ScreenshotRequests",
    "ExecutionRequests",
    "BaselineRequests",
    "MetricRequests",
    "AnglesRequests",
]
