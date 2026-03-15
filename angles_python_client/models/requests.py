from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .action import Action
from .platform import Platform
from .ignore_box import IgnoreBox


@dataclass
class CreateBuild:
    environment: str
    team: str
    component: str
    name: str
    start: Optional[_dt.datetime] = None
    phase: Optional[str] = None


@dataclass
class CreateExecution:
    title: str
    suite: str
    build: str
    feature: Optional[str] = None
    actions: Optional[List[Action]] = None
    platforms: Optional[List[Platform]] = None
    tags: Optional[List[str]] = None
    meta: Optional[Dict[str, Any]] = None


@dataclass
class CreateEnvironment:
    name: str


@dataclass
class CreateTeam:
    name: str
    components: Optional[List[Dict[str, Any]]] = None


@dataclass
class ScreenshotPlatform:
    platformName: Optional[str] = None
    platformVersion: Optional[str] = None
    browserName: Optional[str] = None
    browserVersion: Optional[str] = None
    deviceName: Optional[str] = None


@dataclass
class StoreScreenshot:
    buildId: str
    view: str
    timestamp: _dt.datetime
    filePath: str
    tags: Optional[List[str]] = None
    platform: Optional[ScreenshotPlatform] = None
