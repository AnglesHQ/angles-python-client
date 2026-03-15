from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class AnglesApiError(RuntimeError):
    """Raised when Angles API returns non-2xx."""

    message: str
    status_code: Optional[int] = None
    url: Optional[str] = None
    response_text: Optional[str] = None

    def __str__(self) -> str:
        parts = [self.message]
        if self.status_code is not None:
            parts.append(f"status={self.status_code}")
        if self.url:
            parts.append(f"url={self.url}")
        if self.response_text:
            parts.append(f"response={self.response_text[:500]}")
        return " | ".join(parts)
