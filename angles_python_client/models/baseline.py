from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .ignore_box import IgnoreBox
from .platform import Platform
from .screenshot import Screenshot


@dataclass
class Baseline:
    screenshot: Optional[Screenshot] = None
    view: Optional[str] = None
    platform: Optional[Platform] = None
    screenHeight: Optional[int] = None
    screenWidth: Optional[int] = None
    ignoreBoxes: Optional[List[IgnoreBox]] = None
