# src/OPE_IsoGen/Geometry/Iso/ellipse_iso.py
from __future__ import annotations
import math
from typing import List, Tuple
from ..Contracts.circle_spec import CircleSpec
from ..Contracts.ellipse_spec import EllipseSpec
from .projector_top import iso_project_point

Pt2 = Tuple[float,float]
Pt3 = Tuple[float,float,float]

def _unit(v: Pt3) -> Pt3:
    L = math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2]) or 1.0
    return (v[0]/L, v[1]/L, v[2]/L)

def _basis_from_normal(n: Pt3):
    nx, ny, nz = n
    if abs(nx) < 0.9: ref = (1.0,0.0,0.0)
    elif abs(ny) < 0.9: ref = (0.0,1.0,0.0)
    else: ref = (0.0,0.0,1.0)
    # u = unit(n x ref)
    ux = ny*ref[2] - nz*ref[1]
    uy = nz*ref[0] - nx*ref[2]
    uz = nx*ref[1] - ny*ref[0]
    u = _unit((ux,uy,uz))
    # v = n x u
    vx = ny*u[2] - nz*u[1]
    vy = nz*u[0] - nx*u[2]
    vz = nx*u[1] - ny*u[0]
    v = _unit((vx,vy,vz))
    return u, v

def iso_ellipse_from_circle(spec: CircleSpec, segments: int = 96) -> List[Pt2]:
    """Sample 2D ellipse (ISO) from 3D circle (center/normal/R)."""
    if spec.R <= 0 or segments < 8: return []
    u, v = _basis_from_normal(spec.n)
    cx, cy, cz = spec.C
    out: List[Pt2] = []
    for i in range(segments+1):
        t = 2*math.pi * i / segments
        px = cx + spec.R*(u[0]*math.cos(t) + v[0]*math.sin(t))
        py = cy + spec.R*(u[1]*math.cos(t) + v[1]*math.sin(t))
        pz = cz + spec.R*(u[2]*math.cos(t) + v[2]*math.sin(t))
        out.append(iso_project_point(px,py,pz))
    return out

def iso_ellipse_from_ellipse(spec: EllipseSpec, segments: int = 96) -> List[Pt2]:
    """Sample 2D ellipse (ISO) from 3D ellipse (C,n,xdir,a,b)."""
    if spec.a <= 0 or spec.b <= 0 or segments < 8: return []
    U = _unit(spec.xdir)
    nx, ny, nz = spec.n
    # V = n x U
    V = _unit((ny*U[2]-nz*U[1], nz*U[0]-nx*U[2], nx*U[1]-ny*U[0]))
    cx, cy, cz = spec.C
    out: List[Pt2] = []
    for i in range(segments+1):
        t = 2*math.pi * i / segments
        px = cx + spec.a*(U[0]*math.cos(t)) + spec.b*(V[0]*math.sin(t))
        py = cy + spec.a*(U[1]*math.cos(t)) + spec.b*(V[1]*math.sin(t))
        pz = cz + spec.a*(U[2]*math.cos(t)) + spec.b*(V[2]*math.sin(t))
        out.append(iso_project_point(px,py,pz))
    return out