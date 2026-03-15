from __future__ import annotations

import requests
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.parse import urljoin

from .exceptions import AnglesApiError


@dataclass
class AnglesHttpClient:
    """Thin wrapper around requests.Session with Angles defaults."""

    base_url: str = "http://127.0.0.1:3000/rest/api/v1.0/"
    timeout_s: float = 10.0
    session: Optional[requests.Session] = None
    default_headers: Optional[Dict[str, str]] = None

    def __post_init__(self) -> None:
        if self.session is None:
            self.session = requests.Session()
        if self.default_headers is None:
            self.default_headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }

    def set_base_url(self, base_url: str) -> None:
        if not base_url.endswith("/"):
            base_url += "/"
        self.base_url = base_url

    def _full_url(self, path_or_url: str) -> str:
        # Support absolute URLs (used by MetricRequests).
        if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
            return path_or_url
        return urljoin(self.base_url, path_or_url.lstrip("/"))

    def request(
        self,
        method: str,
        path_or_url: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Any = None,
        data: Any = None,
        files: Any = None,
        headers: Optional[Dict[str, str]] = None,
        timeout_s: Optional[float] = None,
        stream: bool = False,
    ) -> requests.Response:
        url = self._full_url(path_or_url)
        merged_headers: Dict[str, str] = dict(self.default_headers or {})
        if headers:
            merged_headers.update(headers)

        try:
            resp = self.session.request(
                method=method.upper(),
                url=url,
                params=params,
                json=json,
                data=data,
                files=files,
                headers=merged_headers,
                timeout=timeout_s if timeout_s is not None else self.timeout_s,
                stream=stream,
            )
        except requests.RequestException as e:
            raise AnglesApiError(f"Request failed: {e}", url=url) from e

        if not (200 <= resp.status_code < 300):
            # Best effort to include body.
            text = None
            try:
                text = resp.text
            except Exception:
                text = None
            raise AnglesApiError(
                "Angles API returned error",
                status_code=resp.status_code,
                url=url,
                response_text=text,
            )
        return resp
