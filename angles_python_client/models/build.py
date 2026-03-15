from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .artifact import Artifact
from .environment import Environment
from .enums import ExecutionStates
from .team import Team


@dataclass
class Build:
    _id: Optional[str] = None
    name: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    status: Optional[ExecutionStates] = None
    start: Optional[_dt.datetime] = None
    end: Optional[_dt.datetime] = None
    artifacts: Optional[List[Artifact]] = None
    keep: Optional[bool] = None
    environment: Optional[Environment] = None
    team: Optional[Team] = None
    component: Optional[str] = None
    suites: Optional[List[Any]] = None
