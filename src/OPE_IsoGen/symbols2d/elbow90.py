from __future__ import annotations
from dataclasses import dataclass
from typing import List
from .base import Base2DSymbol, ConnectionPoint
from ..geometry2d.primitives import ArcLocal

@dataclass
class Elbow90Params:
    od_mm: float = 100.0
    radius_mm: float | None = None  # CLR; default 1.5 * OD if None

class Elbow90_2D(Base2DSymbol):
    """
    90-degree elbow turning from +X to +Y, as centerline arc in local space.
    CPs:
      - inlet  at (R,0)  dir 0°
      - outlet at (0,R)  dir 90°
    """
    def __init__(self, p: Elbow90Params | None = None):
        self.p = p or Elbow90Params()
        if self.p.radius_mm is None:
            self.p.radius_mm = 1.5 * self.p.od_mm

    def geometry_local(self) -> List:
        R = self.p.radius_mm
        return [ArcLocal(0.0, 0.0, R, 0.0, 90.0, layer="centerline")]

    def connection_points_local(self):
        R = self.p.radius_mm
        return [
            ConnectionPoint("inlet",  R, 0.0,   0.0,  "inlet"),
            ConnectionPoint("outlet", 0.0, R,  90.0, "outlet"),
        ]