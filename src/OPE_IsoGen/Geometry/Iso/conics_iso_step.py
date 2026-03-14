# src/OPE_IsoGen/Geometry/Iso/conics_iso.py
from __future__ import annotations
import math
from typing import List, Tuple

Pt2 = Tuple[float,float]

def iso_param_ellipse(center_xy: Pt2, a: float, b: float, xdir_angle_deg: float = 0.0, segments: int = 96) -> List[Pt2]:
    """Pure 2D ellipse param sampling (ISO plane), useful for preview."""
    if a <= 0 or b <= 0 or segments < 8: return []
    cx, cy = center_xy
    ang = math.radians(xdir_angle_deg)
    ca, sa = math.cos(ang), math.sin(ang)
    out: List[Pt2] = []
    for i in range(segments+1):
        t = 2*math.pi * i / segments
        x = a*math.cos(t)
        y = b*math.sin(t)
        # rotate by xdir_angle
        xr = ca*x - sa*y
        yr = sa*x + ca*y
        out.append((cx + xr, cy + yr))
    return out