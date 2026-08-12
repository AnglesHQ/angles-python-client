from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CompareOptions:
    """Options for the screenshot compare endpoints.

    Field names match the API's query parameters.
    """

    # Comparison algorithm: 'pixel' (default), 'ssim', or 'phash' (JSON endpoints only).
    algorithm: Optional[str] = None
    # Per-pixel colour-distance threshold (0-1, pixel algorithm only). Defaults to 0.5.
    threshold: Optional[float] = None
    # When true (pixel algorithm only), changed pixels are clustered into regions.
    regions: Optional[bool] = None


@dataclass
class DiffRegion:
    x: Optional[int] = None
    y: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    # Number of changed pixels inside the region.
    pixels: Optional[int] = None
