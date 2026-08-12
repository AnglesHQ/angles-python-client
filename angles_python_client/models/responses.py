from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .build import Build
from .execution import Execution
from .requests import ScreenshotPlatform


@dataclass
class DefaultResponse:
    message: Optional[str] = None


@dataclass
class BuildsResponse:
    count: Optional[int] = None
    builds: Optional[List[Build]] = None


@dataclass
class ExecutionResponse:
    count: Optional[int] = None
    builds: Optional[List[Execution]] = None  # kept as 'builds' for like-for-like


@dataclass
class ImageCompareResponse:
    # Algorithm that produced this result: 'pixel', 'ssim', or 'phash'.
    algorithm: Optional[str] = None
    isSameDimensions: Optional[bool] = None
    rawMisMatchPercentage: Optional[float] = None
    misMatchPercentage: Optional[float] = None
    analysisTime: Optional[float] = None
    # SSIM score in [-1, 1] (1 = identical); present when algorithm is 'ssim'.
    ssim: Optional[float] = None
    # Normalised perceptual-hash distance (0-1); present when algorithm is 'phash'.
    distance: Optional[float] = None
    # Clustered change regions; present when requested with regions=true (pixel only).
    regions: Optional[List[Any]] = None


@dataclass
class Period:
    groupId: Optional[int] = None
    start: Optional[_dt.datetime] = None
    end: Optional[_dt.datetime] = None
    result: Optional[Dict[str, Any]] = None
    buildCount: Optional[int] = None
    phases: Optional[List[Any]] = None


@dataclass
class PhaseMetrics:
    toDate: Optional[_dt.date] = None
    fromDate: Optional[_dt.date] = None
    groupingPeriod: Optional[str] = None
    periods: Optional[List[Period]] = None


@dataclass
class ScreenshotMetric:
    _id: Optional[str] = None
    count: Optional[int] = None
    platforms: Optional[List[ScreenshotPlatform]] = None


@dataclass
class ScreenshotMetrics:
    views: Optional[List[ScreenshotMetric]] = None
    tags: Optional[List[ScreenshotMetric]] = None
