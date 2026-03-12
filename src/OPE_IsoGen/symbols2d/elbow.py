from __future__ import annotations
from dataclasses import dataclass
import math
from typing import List

from .base import Base2DSymbol, ConnectionPoint
from ..geometry2d.primitives import ArcLocal

@dataclass
class ElbowParams:
    od_mm: float = 100.0
    angle_deg: float = 90.0     # could be 45 or 90
    radius_mm: float | None = None

class Elbow2D(Base2DSymbol):

    SKEY = "ELBW"

    def __init__(self, p: ElbowParams | None = None):
        self.p = p or ElbowParams()

        # default CLR = 1.5 x OD
        if self.p.radius_mm is None:
            self.p.radius_mm = 1.5 * self.p.od_mm

        if self.p.angle_deg not in (45, 90):
            raise ValueError("Elbow angle must be 45 or 90")

        self.R = self.p.radius_mm
        self.theta = self.p.angle_deg

    def geometry_local(self) -> List:
        """Return local elbow arc (flat XY local coords)."""
        return [
            ArcLocal(
                cx=0.0,
                cy=0.0,
                r=self.R,
                start_deg=0.0,
                end_deg=self.theta,
                layer="centerline"
            )
        ]

    def connection_points_local(self):
        R = self.R
        θ = self.theta

        # inlet at (R, 0)
        inlet = ConnectionPoint(
            name="inlet",
            x=R,
            y=0.0,
            dir_deg=180.0,   # pointing LEFT
            kind="inlet"
        )

        # outlet at (R*cosθ, R*sinθ)
        ox = R * math.cos(math.radians(θ))
        oy = R * math.sin(math.radians(θ))
        out_dir = (180.0 + θ) % 360.0

        outlet = ConnectionPoint(
            name="outlet",
            x=ox,
            y=oy,
            dir_deg=out_dir,
            kind="outlet"
        )

        # center (not used for connection)
        center = ConnectionPoint("center", 0.0, 0.0, None, "center")

        return [center, inlet, outlet]