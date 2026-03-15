from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import datetime as _dt

@dataclass
class Versions:
    node: Optional[str] = None
    mongo: Optional[str] = None
    angles: Optional[str] = None
