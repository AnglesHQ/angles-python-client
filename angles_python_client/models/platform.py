from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import datetime as _dt

@dataclass
class Platform:
    _id: Optional[str] = None
    platformName: Optional[str] = None
    platformVersion: Optional[str] = None
    browserName: Optional[str] = None
    browserVersion: Optional[str] = None
    deviceName: Optional[str] = None
    userAgent: Optional[str] = None
    screenHeight: Optional[int] = None
    screenWidth: Optional[int] = None
    pixelRatio: Optional[float] = None
