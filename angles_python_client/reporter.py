from __future__ import annotations

import datetime as _dt
from typing import Any, Dict, List, Optional

from .http import AnglesHttpClient
from .models import Action, Platform, Step, StepStates
from .models.requests import CreateBuild, CreateExecution, StoreScreenshot, ScreenshotPlatform
from .requests import (
    BuildRequests,
    TeamRequests,
    EnvironmentRequests,
    ExecutionRequests,
    ScreenshotRequests,
)


class AnglesReporter:
    """High-level reporter mirroring `AnglesReporterClass` from the JS client.

    The module-level ``angles_reporter`` object remains available as a convenience singleton,
    but ``AnglesReporter`` itself is now safe to instantiate directly. This allows callers to
    maintain isolated build/execution state when they need more than one live reporter.
    """

    _instance: Optional["AnglesReporter"] = None

    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        timeout_s: float = 10.0,
        session: Any = None,
        default_headers: Optional[Dict[str, str]] = None,
    ) -> None:
        self.http = AnglesHttpClient(
            base_url=base_url or AnglesHttpClient.base_url,
            timeout_s=timeout_s,
            session=session,
            default_headers=default_headers,
        )
        self._instantiate_clients()

        self.current_build: Optional[Dict[str, Any]] = None
        self.current_execution: Optional[CreateExecution] = None
        self.current_action: Optional[Action] = None

    def _instantiate_clients(self) -> None:
        self.teams = TeamRequests(self.http)
        self.environments = EnvironmentRequests(self.http)
        self.builds = BuildRequests(self.http)
        self.executions = ExecutionRequests(self.http)
        self.screenshots = ScreenshotRequests(self.http)

    @classmethod
    def get_instance(cls) -> "AnglesReporter":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def get_instance_with_base_url(cls, base_url: str) -> "AnglesReporter":
        """Backward-compatible convenience helper.

        Returns a new reporter bound to ``base_url`` so callers do not share mutable build/test
        state accidentally. Use ``get_instance()`` or the module-level ``angles_reporter`` when a
        process-wide convenience singleton is actually desired.
        """
        return cls(base_url=base_url)

    def set_base_url(self, base_url: str) -> None:
        self.http.set_base_url(base_url)

    def reset_state(self) -> None:
        """Clear tracked build/execution/action state without recreating the HTTP client."""
        self.current_build = None
        self.current_execution = None
        self.current_action = None

    def set_current_build(self, build_id: str) -> None:
        self.current_build = self.current_build or {}
        self.current_build["_id"] = build_id

    # --- build lifecycle ---
    def start_build(self, name: str, team: str, environment: str, component: str, phase: Optional[str] = None) -> Dict[str, Any]:
        req = CreateBuild(
            name=name,
            team=team,
            environment=environment,
            component=component,
            phase=phase,
            start=_dt.datetime.now(),
        )
        created = self.builds.create_build(req)
        self.current_build = created
        return created

    def add_artifacts(self, artifacts: List[Any]) -> Any:
        if not self.current_build or not self.current_build.get("_id"):
            raise RuntimeError("No current build set. Call start_build() or set_current_build() first.")
        return self.builds.add_artifacts(self.current_build["_id"], artifacts)

    # --- execution lifecycle ---
    def start_test(self, title: str, suite: str) -> None:
        if not self.current_build or not self.current_build.get("_id"):
            raise RuntimeError("No current build set. Call start_build() or set_current_build() first.")
        self.current_execution = CreateExecution(
            title=title,
            suite=suite,
            build=self.current_build["_id"],
            actions=[],
            platforms=[],
        )
        self.current_action = None

    def update_test_name(self, title: str, suite: Optional[str] = None) -> None:
        if self.current_execution:
            self.current_execution.title = title
            if suite:
                self.current_execution.suite = suite

    def store_platform_details(self, platform: Platform) -> None:
        if self.current_execution:
            if self.current_execution.platforms is None:
                self.current_execution.platforms = []
            self.current_execution.platforms.append(platform)

    def save_test(self) -> Any:
        if not self.current_execution:
            raise RuntimeError("No current test started. Call start_test() first.")
        return self.executions.save_execution(self.current_execution)

    # --- screenshots ---
    def save_screenshot(self, file_path: str, view: str, tags: Optional[List[str]] = None) -> Any:
        return self.save_screenshot_with_platform(file_path=file_path, view=view, tags=tags, platform=None)

    def save_screenshot_with_platform(
        self,
        file_path: str,
        view: str,
        tags: Optional[List[str]] = None,
        platform: Optional[ScreenshotPlatform] = None,
    ) -> Any:
        if not self.current_build or not self.current_build.get("_id"):
            raise RuntimeError("No current build set. Call start_build() or set_current_build() first.")
        store = StoreScreenshot(
            buildId=self.current_build["_id"],
            filePath=file_path,
            view=view,
            timestamp=_dt.datetime.now(),
            tags=tags,
            platform=platform,
        )
        return self.screenshots.save_screenshot(store)

    def compare_screenshot_against_baseline(self, screenshot_id: str) -> Any:
        return self.screenshots.get_baseline_compare(screenshot_id)

    # --- steps/actions ---
    def add_action(self, name: str) -> None:
        self.current_action = Action(name=name, start=_dt.datetime.now(), steps=[])
        if self.current_execution is None:
            # JS uses a default Set-up execution if you start logging early
            self.start_test("Set-up", "Set-up")
        assert self.current_execution is not None
        if self.current_execution.actions is None:
            self.current_execution.actions = []
        self.current_execution.actions.append(self.current_action)

    def _ensure_action(self) -> None:
        if self.current_action is None:
            self.add_action("test-details")

    def info(self, info: str) -> None:
        self.add_step(name="INFO", expected=None, actual=None, info=info, status=StepStates.INFO, screenshot=None)

    def debug(self, info: str) -> None:
        self.add_step(name="DEBUG", expected=None, actual=None, info=info, status=StepStates.DEBUG, screenshot=None)

    def info_with_screenshot(self, info: str, screenshot_id: str) -> None:
        self.add_step(name="INFO", expected=None, actual=None, info=info, status=StepStates.INFO, screenshot=screenshot_id)

    def error(self, error: str) -> None:
        self.add_step(name="ERROR", expected=None, actual=None, info=error, status=StepStates.ERROR, screenshot=None)

    def error_with_screenshot(self, error: str, screenshot_id: str) -> None:
        self.add_step(name="ERROR", expected=None, actual=None, info=error, status=StepStates.ERROR, screenshot=screenshot_id)

    # `pass` is a keyword in python
    def pass_step(self, name: str, expected: str, actual: str, info: str) -> None:
        self.add_step(name=name, expected=expected, actual=actual, info=info, status=StepStates.PASS, screenshot=None)

    def pass_with_screenshot(self, name: str, expected: str, actual: str, info: str, screenshot_id: str) -> None:
        self.add_step(name=name, expected=expected, actual=actual, info=info, status=StepStates.PASS, screenshot=screenshot_id)

    def fail_step(self, name: str, expected: str, actual: str, info: str) -> None:
        self.add_step(name=name, expected=expected, actual=actual, info=info, status=StepStates.FAIL, screenshot=None)

    def fail_with_screenshot(self, name: str, expected: str, actual: str, info: str, screenshot_id: str) -> None:
        self.add_step(name=name, expected=expected, actual=actual, info=info, status=StepStates.FAIL, screenshot=screenshot_id)

    def add_step(
        self,
        name: str,
        expected: Optional[str],
        actual: Optional[str],
        info: Optional[str],
        status: StepStates,
        screenshot: Optional[str],
    ) -> None:
        self._ensure_action()
        assert self.current_action is not None
        step = Step(
            name=name,
            expected=expected,
            actual=actual,
            info=info,
            status=status,
            timestamp=_dt.datetime.now(),
            screenshot=screenshot,
        )
        if self.current_action.steps is None:
            self.current_action.steps = []
        self.current_action.steps.append(step)


angles_reporter = AnglesReporter.get_instance()
