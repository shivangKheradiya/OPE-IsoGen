from __future__ import annotations
from dataclasses import dataclass
from typing import List
from .base import Base2DSymbol, ConnectionPoint
from ..geometry2d.primitives import Line2D

@dataclass
class StraightPipe2DParams:
    od_mm: float = 100.0
    length_mm: float = 500.0

class StraightPipe2D(Base2DSymbol):
    """
    Centerline representation along +X direction.
    Connection points:
      - inlet  at (0, 0), dir 0°
      - outlet at (L, 0), dir 0°
    """

    def __init__(self, p: StraightPipe2DParams | None = None):
        self.p = p or StraightPipe2DParams()

    def geometry_local(self) -> List:
        # Centerline from (0,0) to (L,0)
        L = self.p.length_mm
        return [Line2D(0, 0, L, 0, layer="centerline")]

    def connection_points_local(self):
        L = self.p.length_mm
        return [
            ConnectionPoint("inlet", 0.0, 0.0, dir_deg=0.0, kind="inlet"),
            ConnectionPoint("outlet", L,   0.0, dir_deg=0.0, kind="outlet"),
        ]
