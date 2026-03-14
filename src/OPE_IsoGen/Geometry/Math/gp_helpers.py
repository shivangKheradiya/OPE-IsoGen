from __future__ import annotations
from typing import Tuple, Optional
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir, gp_Ax2

Pt3 = Tuple[float, float, float]

def as_pnt(p: Pt3 | gp_Pnt) -> gp_Pnt:
    return p if isinstance(p, gp_Pnt) else gp_Pnt(float(p[0]), float(p[1]), float(p[2]))

def as_vec(v: Pt3 | gp_Vec) -> gp_Vec:
    return v if isinstance(v, gp_Vec) else gp_Vec(float(v[0]), float(v[1]), float(v[2]))

def unit_vec(v: gp_Vec, tol: float = 1e-12) -> gp_Vec:
    g = gp_Vec(v.X(), v.Y(), v.Z())
    if g.Magnitude() < tol:  # fallback up
        return gp_Vec(0, 0, 1)
    g.Normalize()
    return g

def plane_ax2(C: Pt3 | gp_Pnt, n: Pt3 | gp_Vec, xdir_hint: Optional[Pt3 | gp_Vec] = None) -> gp_Ax2:
    """Robust gp_Ax2(center, normal, XDir) in the circle plane."""
    C_p = as_pnt(C)
    n_v = unit_vec(as_vec(n))
    ref = gp_Vec(1,0,0) if abs(n_v.X()) < 0.9 else gp_Vec(0,1,0)

    # project ref into the plane: xdir = ref - (ref·n_v) * n_v
    dot = ref.Dot(n_v)
    xdir = gp_Vec(ref.X() - dot * n_v.X(),
                  ref.Y() - dot * n_v.Y(),
                  ref.Z() - dot * n_v.Z())

    if xdir.Magnitude() < 1e-12:
        xdir = gp_Vec(0, 1, 0)
    xdir.Normalize()
    return gp_Ax2(as_pnt(C), gp_Dir(n_v), gp_Dir(xdir))
