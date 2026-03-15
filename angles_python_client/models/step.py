from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass
from typing import Optional

from .enums import StepStates


@dataclass
class Step:
    name: Optional[str] = None
    expected: Optional[str] = None
    actual: Optional[str] = None
    info: Optional[str] = None
    status: Optional[StepStates] = None
    timestamp: Optional[_dt.datetime] = None
    screenshot: Optional[str] = None
