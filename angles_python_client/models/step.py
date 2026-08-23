from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass
from typing import List, Optional

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
    #: Attachment ids referenced by a manual step result.
    attachments: Optional[List[str]] = None
