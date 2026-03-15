from __future__ import annotations

import datetime as _dt
from dataclasses import asdict
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

from ._serialize import jsonable, json_dumps
from .http import AnglesHttpClient
from .models.enums import GroupingPeriods


class BaseRequests:
    def __init__(self, http: AnglesHttpClient):
        self.http = http

    def _json(self, obj: Any) -> Any:
        return jsonable(obj)

    def post(self, url: str, body: Any, *, headers: Optional[Dict[str, str]] = None) -> Any:
        resp = self.http.request("POST", url, json=self._json(body), headers=headers)
        return resp.json() if resp.content else None

    def get(self, url: str, *, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, response_type: str = "json") -> Any:
        resp = self.http.request("GET", url, params=params, headers=headers, stream=(response_type=="bytes"))
        if response_type == "bytes":
            return resp.content
        return resp.json() if resp.content else None

    def put(self, url: str, body: Any = None, *, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Any:
        resp = self.http.request("PUT", url, params=params, json=self._json(body) if body is not None else None, headers=headers)
        return resp.json() if resp.content else None

    def delete(self, url: str, *, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Any:
        resp = self.http.request("DELETE", url, params=params, headers=headers)
        return resp.json() if resp.content else None


class TeamRequests(BaseRequests):
    def create_team(self, request: Any) -> Any:
        return self.post("team", request)

    def get_teams(self) -> Any:
        return self.get("team")

    def get_team(self, team_id: str) -> Any:
        return self.get(f"team/{team_id}")

    def delete_team(self, team_id: str) -> Any:
        return self.delete(f"team/{team_id}")

    def update_team(self, team_id: str, name: str) -> Any:
        return self.put(f"team/{team_id}", {"name": name})

    def add_components_to_team(self, team_id: str, components: List[str]) -> Any:
        return self.put(f"team/{team_id}", {"components": components})


class EnvironmentRequests(BaseRequests):
    def create_environment(self, request: Any) -> Any:
        return self.post("environment", request)

    def get_environment(self, environment_id: str) -> Any:
        return self.get(f"environment/{environment_id}")

    def get_environments(self) -> Any:
        return self.get("environment")

    def delete_environment(self, environment_id: str) -> Any:
        return self.delete(f"environment/{environment_id}")

    def update_environment(self, environment_id: str, name: str) -> Any:
        return self.put(f"environment/{environment_id}", {"name": name})


class BuildRequests(BaseRequests):
    def create_build(self, request: Any) -> Any:
        return self.post("build", request)

    def get_builds(self, team_id: str, build_ids: Optional[List[str]] = None, return_execution_details: bool = False) -> Any:
        # matches JS: /build?teamId=...&buildIds=...&returnExecutionDetails=...
        params: Dict[str, Any] = {"teamId": team_id}
        if build_ids:
            params["buildIds"] = ",".join(build_ids)
        if return_execution_details:
            params["returnExecutionDetails"] = "true"
        return self.get("build", params=params)

    def get_builds_with_filters(self, team_id: str, filter_environments: Optional[List[str]] = None, filter_components: Optional[List[str]] = None, skip: int = 0, limit: int = 50) -> Any:
        params: Dict[str, Any] = {"teamId": team_id, "skip": skip, "limit": limit}
        if filter_environments:
            params["environmentIds"] = ",".join(filter_environments)
        if filter_components:
            params["componentIds"] = ",".join(filter_components)
        return self.get("build", params=params)

    def get_builds_with_date_filters(
        self,
        team_id: str,
        filter_environments: Optional[List[str]] = None,
        filter_components: Optional[List[str]] = None,
        skip: int = 0,
        limit: int = 50,
        from_date: Optional[_dt.date] = None,
        to_date: Optional[_dt.date] = None,
    ) -> Any:
        params: Dict[str, Any] = {"teamId": team_id, "skip": skip, "limit": limit}
        if from_date:
            params["fromDate"] = from_date.isoformat()
        if to_date:
            params["toDate"] = to_date.isoformat()
        if filter_environments:
            params["environmentIds"] = ",".join(filter_environments)
        if filter_components:
            params["componentIds"] = ",".join(filter_components)
        return self.get("build", params=params)

    def delete_builds(self, team_id: str, age_in_days: int) -> Any:
        return self.delete("build", params={"teamId": team_id, "ageInDays": age_in_days})

    def get_build(self, build_id: str) -> Any:
        return self.get(f"build/{build_id}")

    def get_build_report(self, build_id: str) -> Any:
        return self.get(f"build/{build_id}/report")

    def delete_build(self, build_id: str) -> Any:
        return self.delete(f"build/{build_id}")

    def set_keep(self, build_id: str, keep: bool) -> Any:
        return self.put(f"build/{build_id}/keep", {"keep": keep})

    def add_artifacts(self, build_id: str, artifacts: List[Any]) -> Any:
        return self.put(f"build/{build_id}/artifacts", {"artifacts": artifacts})


class ExecutionRequests(BaseRequests):
    def save_execution(self, save_execution_request: Any) -> Any:
        return self.post("execution/", save_execution_request)

    def get_execution(self, execution_id: str) -> Any:
        return self.get(f"execution/{execution_id}")

    def delete_execution(self, execution_id: str) -> Any:
        return self.delete(f"execution/{execution_id}")

    def get_execution_history(self, execution_id: str, skip: int = 0, limit: int = 50) -> Any:
        return self.get(f"execution/{execution_id}/history", params={"skip": skip, "limit": limit})


class ScreenshotRequests(BaseRequests):
    def save_screenshot(self, store_screenshot: Any) -> Any:
        # multipart form-data
        import os
        import json as _json

        payload = jsonable(store_screenshot)
        full_path = os.path.abspath(payload["filePath"])
        file_name = os.path.basename(full_path)

        data: Dict[str, Any] = {
            "buildId": payload["buildId"],
            "view": payload["view"],
            "timestamp": payload["timestamp"] if isinstance(payload["timestamp"], str) else str(payload["timestamp"]),
        }
        if payload.get("tags") is not None:
            data["tags"] = _json.dumps(payload["tags"])
        platform = payload.get("platform")
        if platform:
            for k, v in platform.items():
                if v is not None:
                    data[k] = v

        with open(full_path, "rb") as f:
            files = {"screenshot": (file_name, f)}
            # IMPORTANT: when using files=..., don't set Content-Type json
            headers = {"Accept": "application/json"}
            resp = self.http.request("POST", "screenshot/", data=data, files=files, headers=headers)
            return resp.json() if resp.content else None

    def get_screenshots_for_build(self, build_id: str, limit: int = 100) -> Any:
        params: Dict[str, Any] = {"buildId": build_id}
        if limit:
            params["limit"] = limit
        return self.get("screenshot/", params=params)

    def get_screenshots(self, screenshot_ids: List[str]) -> Any:
        return self.get("screenshot/", params={"screenshotIds": ",".join(screenshot_ids)})

    def get_screenshot_views(self, view: str, limit: int = 50) -> Any:
        return self.get("screenshot/views", params={"view": view, "limit": limit})

    def get_screenshot_tags(self, tag: str, limit: int = 50) -> Any:
        return self.get("screenshot/tags", params={"tag": tag, "limit": limit})

    def get_screenshot_history_by_view(self, view: str, platform_id: str, limit: int = 50, offset: int = 0) -> Any:
        return self.get("screenshot/", params={"view": view, "platformId": platform_id, "limit": limit, "offset": offset})

    def get_screenshots_grouped_by_platform(self, view: str, number_of_days: int) -> Any:
        return self.get("screenshot/grouped/platform", params={"view": view, "numberOfDays": number_of_days})

    def get_screenshots_grouped_by_tag(self, tag: str, number_of_days: int) -> Any:
        return self.get("screenshot/grouped/tag", params={"tag": tag, "numberOfDays": number_of_days})

    def get_screenshot(self, screenshot_id: str) -> Any:
        return self.get(f"screenshot/{screenshot_id}")

    def delete_screenshot(self, screenshot_id: str) -> Any:
        return self.delete(f"screenshot/{screenshot_id}")

    def get_screenshot_image(self, screenshot_id: str) -> bytes:
        return self.get(f"screenshot/{screenshot_id}/image", response_type="bytes")

    def get_dynamic_baseline_image(self, screenshot_id: str, number_of_images_to_compare: Optional[int] = None) -> Any:
        path = f"screenshot/{screenshot_id}/dynamic-baseline"
        params = {}
        if number_of_images_to_compare and number_of_images_to_compare > 0:
            params["numberOfImagesToCompare"] = number_of_images_to_compare
        return self.get(path, params=params or None)

    def get_baseline_compare_image(self, screenshot_id: str, cache: bool = False) -> bytes:
        return self.get(
            "screenshot/{}/baseline/compare/image/".format(screenshot_id),
            params={"useCache": str(bool(cache)).lower()},
            response_type="bytes",
        )

    def get_baseline_compare(self, screenshot_id: str) -> Any:
        return self.get(f"screenshot/{screenshot_id}/baseline/compare/")


class BaselineRequests(BaseRequests):
    def set_baseline(self, screenshot: Dict[str, Any]) -> Any:
        view = screenshot.get("view")
        screenshot_id = screenshot.get("_id")
        return self.post("baseline", {"view": view, "screenshotId": screenshot_id})

    def get_baseline_for_screenshot(self, screenshot: Dict[str, Any]) -> Any:
        platform = (screenshot.get("platform") or {})
        params: Dict[str, Any] = {
            "view": screenshot.get("view"),
            "platformName": platform.get("platformName"),
        }
        device_name = platform.get("deviceName")
        if device_name:
            params["deviceName"] = device_name
        else:
            params["browserName"] = platform.get("browserName")
            params["screenHeight"] = screenshot.get("height")
            params["screenWidth"] = screenshot.get("width")
        return self.get("baseline/", params=params)

    def get_baselines(self) -> Any:
        return self.get("baseline")

    def get_baseline(self, baseline_id: str) -> Any:
        return self.get(f"baseline/{baseline_id}")

    def delete_baseline(self, baseline_id: str) -> Any:
        return self.delete(f"baseline/{baseline_id}")

    def update_baseline(self, baseline_id: str, screenshot_id: Optional[str] = None, ignore_boxes: Optional[List[Any]] = None) -> Any:
        body: Dict[str, Any] = {}
        if screenshot_id:
            body["screenshotId"] = screenshot_id
        if ignore_boxes is not None:
            body["ignoreBoxes"] = ignore_boxes
        return self.put(f"baseline/{baseline_id}", body)


class MetricRequests(BaseRequests):
    def get_phase_metrics(
        self,
        team_id: str,
        component_id: Optional[str] = None,
        from_date: Optional[_dt.date] = None,
        to_date: Optional[_dt.date] = None,
        grouping_period: Optional[GroupingPeriods] = None,
    ) -> Any:
        params: Dict[str, Any] = {"teamId": team_id}
        if component_id:
            params["componentId"] = component_id
        if from_date:
            params["fromDate"] = from_date.isoformat()
        if to_date:
            params["toDate"] = to_date.isoformat()
        if grouping_period:
            params["groupingPeriod"] = grouping_period.value if hasattr(grouping_period, "value") else str(grouping_period)
        # JS uses an absolute URL via new URL(baseURL + '/metrics/phase?...')
        # We'll just pass a relative path + params; client will build URL.
        return self.get("metrics/phase", params=params)

    def get_screenshot_metrics(self, view: Optional[str] = None, tag: Optional[str] = None, limit: Optional[int] = None, thumbnail: Optional[bool] = None) -> Any:
        params: Dict[str, Any] = {}
        if view:
            params["view"] = view
        if tag:
            params["tag"] = tag
        if limit is not None:
            params["limit"] = str(limit)
        if thumbnail is not None:
            params["thumbnail"] = str(bool(thumbnail)).lower()
        return self.get("metrics/screenshot", params=params or None)


class AnglesRequests(BaseRequests):
    def get_versions(self) -> Any:
        return self.get("angles/versions")
