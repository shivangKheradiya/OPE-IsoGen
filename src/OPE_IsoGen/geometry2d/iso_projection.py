from __future__ import annotations
import math
from typing import Tuple, List
from .primitives import Line2D, Polyline2D

SQ3_2 = math.sqrt(3)/2.0
E_X = ( SQ3_2,  0.5 )    # 30°
E_Y = (-SQ3_2,  0.5 )    # 150°
E_Z = ( 0.0,   -1.0 )    # 270°

PLANE_BASES = {
    "XY": (E_X, E_Y),
    "YZ": (E_Y, E_Z),
    "ZX": (E_Z, E_X),
}

def rotate_local(u: float, v: float, deg: float) -> Tuple[float,float]:
    a = math.radians(deg)
    return (u*math.cos(a) - v*math.sin(a),
            u*math.sin(a) + v*math.cos(a))

def project_point(u: float, v: float, plane: str, rot_deg: float, tx: float, ty: float) -> Tuple[float,float]:
    # 1) rotate in local
    ur, vr = rotate_local(u, v, rot_deg)
    # 2) map via plane basis
    ex, ey = PLANE_BASES.get(plane.upper(), PLANE_BASES["XY"])
    sx = ur*ex[0] + vr*ey[0] + tx
    sy = ur*ex[1] + vr*ey[1] + ty
    return sx, sy

def project_line(x1,y1,x2,y2, plane, rot_deg, tx, ty) -> Line2D:
    sx1, sy1 = project_point(x1, y1, plane, rot_deg, tx, ty)
    sx2, sy2 = project_point(x2, y2, plane, rot_deg, tx, ty)
    return Line2D(sx1, sy1, sx2, sy2)

def sample_arc_points(cx, cy, r, start_deg, end_deg, n=24) -> List[Tuple[float,float]]:
    # uniform sampling in angle
    pts = []
    if n < 2: n = 2
    total = (end_deg - start_deg)
    for i in range(n+1):
        a = math.radians(start_deg + total * (i/n))
        x = cx + r*math.cos(a)
        y = cy + r*math.sin(a)
        pts.append((x,y))
    return pts

def project_polyline(points: List[Tuple[float,float]], plane, rot_deg, tx, ty) -> Polyline2D:
    out = []
    for (x,y) in points:
        sx, sy = project_point(x, y, plane, rot_deg, tx, ty)
        out.append((sx, sy))
    return Polyline2D(out)