from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple

Pt3 = Tuple[float, float, float]

@dataclass(frozen=True)
class CircleSpec:
    """3D circle: center C, plane normal n, radius R (mm)."""
    C: Pt3
    n: Pt3
    R: float