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
    # Ids of files attached to this step (see AnglesReporter.attach_file_to_last_step).
    attachments: Optional[List[str]] = None
