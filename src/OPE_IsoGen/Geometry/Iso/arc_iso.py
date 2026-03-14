from __future__ import annotations
import math
from typing import List, Tuple
from ..Contracts.arc_spec import ArcSpec
from .projector_top import iso_project_point
from ..Iso.circle_iso import _basis_from_normal

Pt2 = Tuple[float, float]

def iso_arc(spec: ArcSpec, chord_tol_mm: float = 1.0) -> List[Pt2]:
    """Project 3D circular arc to 2D isometric polyline."""
    if spec.R <= 0.0: return []
    u, v = _basis_from_normal(spec.n)
    a0 = math.radians(spec.a0_deg)
    a1 = math.radians(spec.a1_deg)
    sweep = a1 - a0
    # segments ~ proportional to arc length vs circle
    circle_len = 2*math.pi*spec.R
    arc_len = abs(sweep) * spec.R
    nseg = max(4, int(max(1.0, arc_len / max(1e-6, chord_tol_mm))))
    out: List[Pt2] = []
    cx, cy, cz = spec.C
    for i in range(nseg+1):
        t = a0 + sweep * (i / nseg)
        px = cx + spec.R*(u[0]*math.cos(t) + v[0]*math.sin(t))
        py = cy + spec.R*(u[1]*math.cos(t) + v[1]*math.sin(t))
        pz = cz + spec.R*(u[2]*math.cos(t) + v[2]*math.sin(t))
        out.append(iso_project_point(px, py, pz))
    return out