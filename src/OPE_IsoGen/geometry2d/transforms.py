from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Tuple

@dataclass
class Transform2D:
    rot_deg: float = 0.0
    tx: float = 0.0
    ty: float = 0.0

    def apply_point(self, x: float, y: float) -> Tuple[float,float]:
        a = math.radians(self.rot_deg)
        xr =  x*math.cos(a) - y*math.sin(a)
        yr =  x*math.sin(a) + y*math.cos(a)
        return xr + self.tx, yr + self.ty