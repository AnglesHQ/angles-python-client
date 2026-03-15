from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .action import Action
from .build import Build
from .enums import ExecutionStates
from .platform import Platform


@dataclass
class Execution:
    _id: Optional[str] = None
    title: Optional[str] = None
    suite: Optional[str] = None
    feature: Optional[str] = None
    build: Optional[Build] = None
    start: Optional[_dt.datetime] = None
    end: Optional[_dt.datetime] = None
    actions: Optional[List[Action]] = None
    platforms: Optional[List[Platform]] = None
    tags: Optional[List[str]] = None
    meta: Optional[Dict[str, Any]] = None
    status: Optional[ExecutionStates] = None
