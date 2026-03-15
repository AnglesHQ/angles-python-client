from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass
from typing import List, Optional

from .enums import ExecutionStates
from .step import Step


@dataclass
class Action:
    name: Optional[str] = None
    steps: Optional[List[Step]] = None
    status: Optional[ExecutionStates] = None
    start: Optional[_dt.datetime] = None
    end: Optional[_dt.datetime] = None
