from __future__ import annotations
import math
from typing import List, Tuple
from ..Contracts.circle_spec import CircleSpec
from .projector_top import iso_project_point
from ..Math.gp_helpers import as_vec
from ..Math.robust_ops import is_zero

Pt2 = Tuple[float, float]

def _basis_from_normal(n: tuple[float,float,float]) -> tuple[tuple[float,float,float], tuple[float,float,float]]:
    """Return orthonormal (u,v) in plane with normal n (pure python; OK for sampling)."""
    nx, ny, nz = n
    # choose ref not parallel
    if abs(nx) < 0.9: ref = (1.0, 0.0, 0.0)
    elif abs(ny) < 0.9: ref = (0.0, 1.0, 0.0)
    else: ref = (0.0, 0.0, 1.0)
    # u = unit(n x ref)
    ux = ny*ref[2] - nz*ref[1]
    uy = nz*ref[0] - nx*ref[2]
    uz = nx*ref[1] - ny*ref[0]
    um = math.sqrt(ux*ux+uy*uy+uz*uz) or 1.0
    ux, uy, uz = ux/um, uy/um, uz/um
    # v = n x u
    vx = ny*uz - nz*uy
    vy = nz*ux - nx*uz
    vz = nx*uy - ny*ux
    return (ux,uy,uz), (vx,vy,vz)

def _nseg_for_chord_tol(R: float, tol: float) -> int:
    """Compute segments so max chord error <= tol on full circle."""
    tol = max(1e-6, tol)
    if tol >= R: return 12
    # delta = 2*acos(1 - tol/R)
    c = 1.0 - tol/float(R)
    c = min(1.0, max(-1.0, c))
    delta = 2.0 * math.acos(c) if not is_zero(R) else math.pi/6
    steps = max(12, int(math.ceil(2*math.pi / max(1e-3, delta))))
    return steps

def iso_circle(spec: CircleSpec, chord_tol_mm: float = 1.0) -> List[Pt2]:
    """Project 3D circle to 2D isometric polyline (ellipse approx)."""
    if spec.R <= 0.0: return []
    u, v = _basis_from_normal(spec.n)
    nseg = _nseg_for_chord_tol(spec.R, chord_tol_mm)
    out: List[Pt2] = []
    cx, cy, cz = spec.C
    for i in range(nseg+1):
        t = 2*math.pi * i / nseg
        px = cx + spec.R*(u[0]*math.cos(t) + v[0]*math.sin(t))
        py = cy + spec.R*(u[1]*math.cos(t) + v[1]*math.sin(t))
        pz = cz + spec.R*(u[2]*math.cos(t) + v[2]*math.sin(t))
        out.append(iso_project_point(px, py, pz))
    return out
