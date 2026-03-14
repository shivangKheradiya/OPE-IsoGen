from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple

Pt3 = Tuple[float, float, float]

@dataclass(frozen=True)
class ParabolaSpec:
    """
    3D parabola in a plane:
      C     : origin of the conic (used as Ax2 location)
      n     : plane normal
      xdir  : in-plane X direction (parabola axis)
      focal : focal distance (mm)
      t0,t1 : geometric parameter trim bounds (OCCT parabola parameter, not angle)
    """
    C: Pt3
    n: Pt3
    xdir: Pt3
    focal: float
    t0: float
    t1: float
