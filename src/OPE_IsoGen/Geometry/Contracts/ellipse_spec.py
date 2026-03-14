from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple

Pt3 = Tuple[float, float, float]

@dataclass(frozen=True)
class EllipseSpec:
    """
    3D ellipse in a plane:
      C     : center (mm)
      n     : plane normal (need not be unit)
      xdir  : in-plane X axis (major-axis direction, need not be unit)
      a     : major radius (mm)
      b     : minor radius (mm), 0 < b <= a
    """
    C: Pt3
    n: Pt3
    xdir: Pt3
    a: float
    b: float

@dataclass(frozen=True)
class EllipticArcSpec(EllipseSpec):
    """
    Elliptic arc on the same ellipse:
      start_deg, end_deg : ellipse parameter angles (deg), measured from xdir in ellipse plane.
    """
    start_deg: float
    end_deg: float