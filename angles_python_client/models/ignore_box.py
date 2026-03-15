from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import datetime as _dt

@dataclass
class IgnoreBox:
    left: Optional[int] = None
    top: Optional[int] = None
    right: Optional[int] = None
    bottom: Optional[int] = None
