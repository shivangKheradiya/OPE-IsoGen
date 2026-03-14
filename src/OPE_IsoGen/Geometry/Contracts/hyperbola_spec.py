from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple

Pt3 = Tuple[float, float, float]

@dataclass(frozen=True)
class HyperbolaSpec:
    """
    3D hyperbola in a plane:
      C     : center
      n     : plane normal
      xdir  : in-plane X direction (major axis)
      a     : major radius (mm)
      b     : minor radius (mm)
      t0,t1 : param trim bounds (OCCT hyperbola parameter, not angle)
    """
    C: Pt3
    n: Pt3
    xdir: Pt3
    a: float
    b: float
    t0: float
    t1: float