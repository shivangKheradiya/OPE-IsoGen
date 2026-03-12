from __future__ import annotations
from dataclasses import dataclass
import math
from typing import List, Tuple, Iterable

# ---------- Basic 2D Geometry Primitives ----------

@dataclass
class Line2D:
    x1: float; y1: float
    x2: float; y2: float
    layer: str = "centerline"

@dataclass
class Arc2D:
    cx: float; cy: float
    r: float
    start_deg: float
    end_deg: float
    layer: str = "centerline"

@dataclass
class Marker2D:
    x: float; y: float
    label: str = ""
    layer: str = "marker"

# ---------- Transform Utilities ----------

@dataclass
class Transform2D:
    # rotation (deg) + translation (tx, ty)
    rot_deg: float = 0.0
    tx: float = 0.0
    ty: float = 0.0

    def apply_point(self, x: float, y: float) -> Tuple[float, float]:
        a = math.radians(self.rot_deg)
        xr = x * math.cos(a) - y * math.sin(a)
        yr = x * math.sin(a) + y * math.cos(a)
        return xr + self.tx, yr + self.ty

    def apply(self, prim):
        if isinstance(prim, Line2D):
            x1, y1 = self.apply_point(prim.x1, prim.y1)
            x2, y2 = self.apply_point(prim.x2, prim.y2)
            return Line2D(x1, y1, x2, y2, layer=prim.layer)
        if isinstance(prim, Arc2D):
            cx, cy = self.apply_point(prim.cx, prim.cy)
            return Arc2D(cx, cy, prim.r, prim.start_deg + self.rot_deg, prim.end_deg + self.rot_deg, layer=prim.layer)
        if isinstance(prim, Marker2D):
            x, y = self.apply_point(prim.x, prim.y)
            return Marker2D(x, y, label=prim.label, layer=prim.layer)
        return prim

    def apply_all(self, prims: Iterable):
        return [self.apply(p) for p in prims]

# ---------- Helpers ----------

def plane_to_rotation_deg(plane: str) -> float:
    """
    Temporary mapping of target 2D 'plane' to an added rotation.
    Real 3D projection will replace this later.
    """
    p = (plane or "XY").upper()
    if p == "XY": return 0.0
    if p == "YZ": return 90.0
    if p == "ZX": return -90.0
    return 0.0