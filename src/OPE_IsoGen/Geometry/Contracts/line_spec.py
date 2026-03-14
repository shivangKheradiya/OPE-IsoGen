from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple

Pt3 = Tuple[float, float, float]

@dataclass(frozen=True)
class LineSpec:
    """3D line: two points (mm)."""
    S: Pt3
    E: Pt3