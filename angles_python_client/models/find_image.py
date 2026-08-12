from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class FindImageOptions:
    """Options for the 'find template in screenshot' endpoints.

    Field names match the API's query parameters.
    """

    # Minimum confidence (0-1) for a region to count as a match. Defaults to 0.8.
    minConfidence: Optional[float] = None
    # Lower bound of the template scale sweep. Defaults to 0.75.
    scaleMin: Optional[float] = None
    # Upper bound of the template scale sweep. Defaults to 1.25.
    scaleMax: Optional[float] = None
    # Maximum number of matches to return (1-25). Defaults to 1.
    maxMatches: Optional[int] = None
    # Match on luminance only, which is more tolerant of colour differences between devices.
    grayscale: Optional[bool] = None


@dataclass
class ImageFindMatch:
    # Left/top edge of the matched region, in original screenshot pixels.
    x: Optional[int] = None
    y: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    # Normalized cross-correlation score (0-1).
    confidence: Optional[float] = None
    # Template scale at which the match was found.
    scale: Optional[float] = None


@dataclass
class ImageFindResponse:
    matches: Optional[List[ImageFindMatch]] = None
    bestMatch: Optional[ImageFindMatch] = None
    imageDimensions: Optional[Dict[str, int]] = None
    templateDimensions: Optional[Dict[str, int]] = None
    # Search duration in milliseconds.
    analysisTime: Optional[int] = None
