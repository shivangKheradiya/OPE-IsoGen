from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple

Pt3 = Tuple[float, float, float]

@dataclass(frozen=True)
class ArcSpec:
    """3D circular arc: center C, normal n, radius R (mm), start/end angles (deg) in circle's plane."""
    C: Pt3
    n: Pt3
    R: float
    a0_deg: float
    a1_deg: float