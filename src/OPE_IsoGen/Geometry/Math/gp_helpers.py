from __future__ import annotations
from typing import Tuple, Optional
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir, gp_Ax2

Pt3 = Tuple[float, float, float]

def as_pnt(p: Pt3 | gp_Pnt) -> gp_Pnt:
    return p if isinstance(p, gp_Pnt) else gp_Pnt(float(p[0]), float(p[1]), float(p[2]))

def as_vec(v: Pt3 | gp_Vec) -> gp_Vec:
    return v if isinstance(v, gp_Vec) else gp_Vec(float(v[0]), float(v[1]), float(v[2]))

def unit_vec(v: gp_Vec, tol: float = 1e-12) -> gp_Vec:
    g = gp_Vec(v)
    if g.Magnitude() < tol:  # fallback up
        return gp_Vec(0, 0, 1)
    g.Normalize()
    return g

def plane_ax2(C: Pt3 | gp_Pnt, n: Pt3 | gp_Vec, xdir_hint: Optional[Pt3 | gp_Vec] = None) -> gp_Ax2:
    """Robust gp_Ax2(center, normal, XDir) in the circle plane."""
    C_p = as_pnt(C)
    n_v = unit_vec(as_vec(n))
    if xdir_hint is None:
        ref = gp_Vec(1, 0, 0) if abs(n_v.X()) < 0.9 else gp_Vec(0, 1, 0)
    else:
        ref = as_vec(xdir_hint)
        if ref.Magnitude() == 0: ref = gp_Vec(1, 0, 0)
    # project ref into plane to get XDir
    xdir = ref - gp_Vec(n_v).Multiplied(ref.Dot(n_v))
    xdir = unit_vec(xdir) if xdir.Magnitude() > 0 else gp_Vec(0, 1, 0)
    return gp_Ax2(C_p, gp_Dir(n_v), gp_Dir(xdir))