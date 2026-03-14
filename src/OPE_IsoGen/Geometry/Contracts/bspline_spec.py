from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Sequence, Optional

Pt3 = Tuple[float, float, float]

@dataclass(frozen=True)
class BSplineSpec:
    """
    3D BSpline/NURBS curve definition:
      poles    : control points (3D)
      knots    : knot vector
      mults    : multiplicities
      degree   : spline degree
      weights  : optional weights (same length as poles)
      periodic : closed/periodic flag
    """
    poles: Sequence[Pt3]
    knots: Sequence[float]
    mults: Sequence[int]
    degree: int
    weights: Optional[Sequence[float]] = None
    periodic: bool = False
