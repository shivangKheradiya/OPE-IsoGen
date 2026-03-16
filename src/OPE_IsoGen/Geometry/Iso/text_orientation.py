from __future__ import annotations
import math
from typing import Tuple
from OPE_IsoGen.Geometry.Iso.projector_top import iso_project_point

Vec3 = Tuple[float, float, float]
Pt3  = Tuple[float, float, float]

_ALLOWED = (+30.0, -30.0, +90.0, -90.0)

class ISOTextOrientation:
    """
    Compute 2D text rotation for ISO drawings.
    Rule: the final angle MUST be one of {+30, -30, +90, -90} degrees.
    We compute the raw projected angle from (C, xdir) and snap to nearest.
    """

    @staticmethod
    def angle_deg(C: Pt3, xdir: Vec3, extra_rot_deg: float = 0.0) -> float:
        # Project anchor and "C + xdir"
        cx, cy = iso_project_point(*C)
        ux, uy = iso_project_point(C[0] + xdir[0], C[1] + xdir[1], C[2] + xdir[2])

        # Raw 2D angle (atan2)
        dx, dy = (ux - cx), (uy - cy)
        if abs(dx) + abs(dy) < 1e-12:
            raw = 0.0
        else:
            raw = math.degrees(math.atan2(dy, dx))

        # Apply extra rotation first
        raw += float(extra_rot_deg)

        # Snap to closest of {+30, -30, +90, -90}
        best = min(_ALLOWED, key=lambda a: ISOTextOrientation._angle_dist(a, raw))
        return best

    @staticmethod
    def _angle_dist(a: float, b: float) -> float:
        """Shortest absolute distance between angles a, b in degrees."""
        d = (a - b + 180.0) % 360.0 - 180.0
        return abs(d)