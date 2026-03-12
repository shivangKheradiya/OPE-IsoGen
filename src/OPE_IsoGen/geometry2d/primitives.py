from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Line2D:
    x1: float; y1: float
    x2: float; y2: float
    layer: str = "centerline"

@dataclass
class Polyline2D:
    points: List[Tuple[float, float]]
    layer: str = "centerline"

@dataclass
class Marker2D:
    x: float; y: float
    label: str = ""
    layer: str = "marker"

# Arc in LOCAL symbol space (used before projection)
@dataclass
class ArcLocal:
    cx: float; cy: float
    r: float
    start_deg: float
    end_deg: float
    layer: str = "centerline"