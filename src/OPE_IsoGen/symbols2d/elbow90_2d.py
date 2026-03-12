from __future__ import annotations
from dataclasses import dataclass
from typing import List
from .base import Base2DSymbol, ConnectionPoint
from ..geometry2d.primitives import Arc2D

@dataclass
class Elbow90Params:
    od_mm: float = 100.0
    radius_mm: float | None = None  # centerline radius (CLR). If None -> 1.5 * OD

class Elbow90_2D(Base2DSymbol):
    """
    90-degree elbow turning from +X to +Y, drawn as a centerline arc.
    Connection points (local):
      - inlet:  at start of arc (angle 0°), dir 0°
      - outlet: at end   of arc (angle 90°), dir 90°
    """

    def __init__(self, p: Elbow90Params | None = None):
        self.p = p or Elbow90Params()
        if self.p.radius_mm is None:
            self.p.radius_mm = 1.5 * self.p.od_mm

    def geometry_local(self) -> List:
        R = self.p.radius_mm
        # Centerline arc centered at (0,0), from 0° to 90°
        return [Arc2D(0.0, 0.0, R, 0.0, 90.0, layer="centerline")]

    def connection_points_local(self):
        R = self.p.radius_mm
        # Start of arc at (R, 0), end at (0, R), using standard 0° along +X and CCW positive
        return [
            ConnectionPoint("inlet",  R, 0.0, dir_deg=0.0,  kind="inlet"),
            ConnectionPoint("outlet", 0.0, R,  dir_deg=90.0, kind="outlet"),
        ]