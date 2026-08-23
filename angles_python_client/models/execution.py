from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .action import Action
from .build import Build
from .enums import ExecutionStates, ExecutionTypes
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
    #: Server-assigned; "automated" unless this came from a manual test run.
    executionType: Optional[ExecutionTypes] = None
    #: The fields below are populated only on manual executions.
    manualTestCase: Optional[str] = None
    manualTestCaseVersion: Optional[str] = None
    versionNumber: Optional[int] = None
    executedBy: Optional[str] = None
