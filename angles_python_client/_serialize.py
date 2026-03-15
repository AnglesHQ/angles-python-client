from __future__ import annotations

import dataclasses
import datetime as _dt
import json
from enum import Enum
from typing import Any, Mapping, Sequence

def _is_dataclass_instance(obj: Any) -> bool:
    return dataclasses.is_dataclass(obj) and not isinstance(obj, type)

def jsonable(obj: Any) -> Any:
    """Convert common python types (dataclasses, datetime, enums) into JSON-serializable values."""
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, _dt.datetime):
        # mimic JS Date#toJSON (UTC-ish ISO). Keep tzinfo if present.
        return obj.isoformat()
    if isinstance(obj, _dt.date):
        return obj.isoformat()
    if _is_dataclass_instance(obj):
        return {k: jsonable(v) for k, v in dataclasses.asdict(obj).items() if v is not None}
    if isinstance(obj, Mapping):
        return {str(k): jsonable(v) for k, v in obj.items() if v is not None}
    if isinstance(obj, (list, tuple, set)):
        return [jsonable(v) for v in obj]
    # fall back: objects with __dict__
    if hasattr(obj, "__dict__"):
        return {k: jsonable(v) for k, v in vars(obj).items() if v is not None}
    return obj

def json_dumps(obj: Any) -> str:
    return json.dumps(jsonable(obj), separators=(",", ":"), ensure_ascii=False)
