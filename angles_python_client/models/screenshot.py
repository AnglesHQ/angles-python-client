from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass
from typing import List, Optional

from .build import Build
from .platform import Platform


@dataclass
class Screenshot:
    _id: Optional[str] = None
    build: Optional[Build] = None
    thumbnail: Optional[str] = None
    timestamp: Optional[_dt.datetime] = None
    path: Optional[str] = None
    view: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None
    platform: Optional[Platform] = None
    platformId: Optional[str] = None
    tags: Optional[List[str]] = None
