from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import datetime as _dt

@dataclass
class Team:
    _id: Optional[int] = None
    name: Optional[str] = None
    components: Optional[List[Dict[str, Any]]] = None
