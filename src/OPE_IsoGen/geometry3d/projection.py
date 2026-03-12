from __future__ import annotations
import math
from typing import Tuple
from ..geometry2d.primitives import Line2D, Polyline2D

# Standard isometric axes (screen space, pre Y-flip done in SVG exporter)
SQ3_2 = math.sqrt(3)/2.0
E_X = ( SQ3_2,  0.5 )   # 30°
E_Y = (-SQ3_2,  0.5 )   # 150°
E_Z = ( 0.0,   -1.0 )   # 270°

def project_point_iso3d(x: float, y: float, z: float) -> Tuple[float, float]:
    """Project 3D point (X=East, Y=North, Z=Up) to 2D isometric screen coords."""
    sx = x*E_X[0] + y*E_Y[0] + z*E_Z[0]
    sy = x*E_X[1] + y*E_Y[1] + z*E_Z[1]
    return (sx, sy)

def project_line3d(p1, p2) -> Line2D:
    x1,y1 = project_point_iso3d(*p1)
    x2,y2 = project_point_iso3d(*p2)
    return Line2D(x1,y1,x2,y2)

def project_polyline3d(points3d) -> Polyline2D:
    pts2d = [project_point_iso3d(*p) for p in points3d]
    return Polyline2D(pts2d)

def project_point_only(p):
    """Project a single 3D point (x,y,z) to isometric 2D."""
    return project_point_iso3d(p[0], p[1], p[2])