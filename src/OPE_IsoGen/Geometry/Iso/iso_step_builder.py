from __future__ import annotations
import math
from typing import List, Tuple

from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopoDS import TopoDS_Compound

# ---- projector & contracts (existing) ----
from .projector_top import iso_project_point
from ..Contracts.line_spec import LineSpec
from ..Contracts.circle_spec import CircleSpec
from ..Contracts.arc_spec import ArcSpec

# ---- circle polyline helpers you already had ----
from .circle_iso import _basis_from_normal, _nseg_for_chord_tol

# ---- new contracts used below (no analytic deps) ----
from ..Contracts.ellipse_spec import EllipseSpec, EllipticArcSpec
from ..Contracts.bspline_spec import BSplineSpec
from ..Contracts.parabola_spec import ParabolaSpec
from ..Contracts.hyperbola_spec import HyperbolaSpec


# =========================
# Internal helpers (SAFE)
# =========================
def _make_compound() -> TopoDS_Compound:
    comp = TopoDS_Compound()
    BRep_Builder().MakeCompound(comp)
    return comp

def _is_finite2(p: Tuple[float, float]) -> bool:
    return math.isfinite(p[0]) and math.isfinite(p[1])

def _dist2(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.hypot(dx, dy)

def _add_edge_2d_safe(comp: TopoDS_Compound,
                      a2: Tuple[float, float],
                      b2: Tuple[float, float],
                      tol: float = 1e-7):
    """Create 2D edge only if points are finite and not coincident."""
    if (not _is_finite2(a2)) or (not _is_finite2(b2)):
        return
    if _dist2(a2, b2) <= tol:
        return
    mk = BRepBuilderAPI_MakeEdge(gp_Pnt(a2[0], a2[1], 0.0), gp_Pnt(b2[0], b2[1], 0.0))
    # pythonocc exposes IsDone(); guard anyway
    try:
        if hasattr(mk, "IsDone") and not mk.IsDone():
            return
    except Exception:
        pass
    BRep_Builder().Add(comp, mk.Edge())

def _unit3(v: Tuple[float, float, float]) -> Tuple[float, float, float]:
    L = math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2]) or 1.0
    return (v[0]/L, v[1]/L, v[2]/L)

def _cross(a: Tuple[float,float,float], b: Tuple[float,float,float]) -> Tuple[float,float,float]:
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])

def _robust_uv_from_plane(n: Tuple[float,float,float],
                          xdir_hint: Tuple[float,float,float] | None = None) -> tuple[Tuple[float,float,float], Tuple[float,float,float]]:
    """
    Build a robust in‑plane orthonormal basis (U,V) for plane normal n.
    If xdir_hint is nearly parallel to n, we switch to a safe reference axis.
    """
    n_u = _unit3(n)
    if xdir_hint is not None:
        U = _unit3(xdir_hint)
        V = _cross(n_u, U)
        if math.fabs(V[0]) + math.fabs(V[1]) + math.fabs(V[2]) < 1e-12:
            # xdir_hint was parallel to n → choose safe ref
            ref = (1.0, 0.0, 0.0) if abs(n_u[0]) < 0.9 else (0.0, 1.0, 0.0)
            U = _unit3(_cross(ref, n_u))  # perp to n
            V = _cross(n_u, U)
    else:
        # choose U from a safe reference not parallel to n
        ref = (1.0, 0.0, 0.0) if abs(n_u[0]) < 0.9 else (0.0, 1.0, 0.0)
        U = _unit3(_cross(ref, n_u))
        V = _cross(n_u, U)
    # normalize V
    V = _unit3(V)
    return U, V


# =========================================
# EXISTING functions (unchanged signatures)
# =========================================
def iso_step_from_line(spec: LineSpec):
    """Return a TopoDS_Compound with one 2D edge (Z=0) for isometric line."""
    comp = _make_compound()
    a2 = iso_project_point(*spec.S)
    b2 = iso_project_point(*spec.E)
    _add_edge_2d_safe(comp, a2, b2)
    return comp

def iso_step_from_circle(spec: CircleSpec, chord_tol_mm: float = 1.0):
    """Return 2D circle as polyline edges (ellipse) in Z=0 STEP."""
    comp = _make_compound()
    if spec.R <= 0:
        return comp
    u, v = _basis_from_normal(spec.n)
    nseg = _nseg_for_chord_tol(spec.R, chord_tol_mm)
    pts2: List[Tuple[float, float]] = []
    cx, cy, cz = spec.C
    for i in range(nseg + 1):
        t = 2 * math.pi * i / nseg
        px = cx + spec.R * (u[0] * math.cos(t) + v[0] * math.sin(t))
        py = cy + spec.R * (u[1] * math.cos(t) + v[1] * math.sin(t))
        pz = cz + spec.R * (u[2] * math.cos(t) + v[2] * math.sin(t))
        pts2.append(iso_project_point(px, py, pz))
    for i in range(nseg):
        _add_edge_2d_safe(comp, pts2[i], pts2[i + 1])
    return comp

def iso_step_from_arc(spec: ArcSpec, chord_tol_mm: float = 1.0):
    """Return 2D arc as polyline edges (ellipse segment) in Z=0 STEP."""
    comp = _make_compound()
    if spec.R <= 0:
        return comp
    u, v = _basis_from_normal(spec.n)
    a0 = math.radians(spec.a0_deg)
    a1 = math.radians(spec.a1_deg)
    sweep = a1 - a0
    arc_len = abs(sweep) * spec.R
    nseg = max(4, int(max(1.0, arc_len / max(1e-6, chord_tol_mm))))
    pts2: List[Tuple[float, float]] = []
    cx, cy, cz = spec.C
    for i in range(nseg + 1):
        t = a0 + sweep * (i / nseg)
        px = cx + spec.R * (u[0] * math.cos(t) + v[0] * math.sin(t))
        py = cy + spec.R * (u[1] * math.cos(t) + v[1] * math.sin(t))
        pz = cz + spec.R * (u[2] * math.cos(t) + v[2] * math.sin(t))
        pts2.append(iso_project_point(px, py, pz))
    for i in range(nseg):
        _add_edge_2d_safe(comp, pts2[i], pts2[i + 1])
    return comp


# =========================================
# NEW: general ellipse / elliptic arc (polyline, safe)
# =========================================
def iso_step_from_ellipse(spec: EllipseSpec, segments: int = 96):
    """
    ISO ellipse on Z=0 from a general 3D ellipse (C,n,xdir,a,b), sampled to polyline.
    """
    comp = _make_compound()
    if spec.a <= 0.0 or spec.b <= 0.0:
        return comp

    # robust in-plane basis from (n, xdir)
    U, V = _robust_uv_from_plane(spec.n, spec.xdir)
    cx, cy, cz = spec.C

    pts: List[Tuple[float, float]] = []
    N = max(8, segments)
    for i in range(N + 1):
        t = 2.0 * math.pi * i / N
        px = cx + spec.a*(U[0]*math.cos(t)) + spec.b*(V[0]*math.sin(t))
        py = cy + spec.a*(U[1]*math.cos(t)) + spec.b*(V[1]*math.sin(t))
        pz = cz + spec.a*(U[2]*math.cos(t)) + spec.b*(V[2]*math.sin(t))
        pts.append(iso_project_point(px, py, pz))

    # stitch segments safely
    for i in range(len(pts) - 1):
        _add_edge_2d_safe(comp, pts[i], pts[i+1])

    # close only if first/last are not (almost) identical
    if pts and _dist2(pts[-1], pts[0]) > 1e-7:
        _add_edge_2d_safe(comp, pts[-1], pts[0])

    return comp


def iso_step_from_elliptic_arc(spec: EllipticArcSpec, segments: int = 64):
    """
    ISO elliptic arc on Z=0 from a general 3D ellipse + start/end params, sampled to polyline.
    """
    comp = _make_compound()
    if spec.a <= 0.0 or spec.b <= 0.0:
        return comp

    U, V = _robust_uv_from_plane(spec.n, spec.xdir)
    cx, cy, cz = spec.C

    a0 = math.radians(spec.start_deg)
    a1 = math.radians(spec.end_deg)

    pts: List[Tuple[float, float]] = []
    N = max(2, segments)
    for i in range(N + 1):
        t = a0 + (a1 - a0) * (i / N)
        px = cx + spec.a*(U[0]*math.cos(t)) + spec.b*(V[0]*math.sin(t))
        py = cy + spec.a*(U[1]*math.cos(t)) + spec.b*(V[1]*math.sin(t))
        pz = cz + spec.a*(U[2]*math.cos(t)) + spec.b*(V[2]*math.sin(t))
        pts.append(iso_project_point(px, py, pz))

    for i in range(len(pts) - 1):
        _add_edge_2d_safe(comp, pts[i], pts[i+1])

    return comp


# =========================================
# NEW: BSpline / NURBS (polyline preview: join projected poles)
# =========================================
def iso_step_from_bspline(spec: BSplineSpec):
    """
    ISO BSpline/NURBS on Z=0 (polyline: connect projected poles).
    If you later add analytic bspline_iso_step.py, you can switch to a single curve.
    """
    comp = _make_compound()
    if not spec.poles or len(spec.poles) < 2:
        return comp

    pts2 = [ iso_project_point(*P) for P in spec.poles ]
    for i in range(len(pts2) - 1):
        _add_edge_2d_safe(comp, pts2[i], pts2[i+1])
    return comp


# =========================================
# NEW: Conics (parabola / hyperbola) on Z=0 (polyline)
# =========================================
def iso_step_from_parabola(spec: ParabolaSpec, segments: int = 96):
    """
    ISO parabola on Z=0 (polyline), canonical param in the plane (U=xdir^, V=n×U):
        P(t) = C + (t) U + (t^2 / (2f)) V,  t ∈ [t0, t1]
    """
    comp = _make_compound()
    if spec.focal == 0.0:
        return comp

    U, V = _robust_uv_from_plane(spec.n, spec.xdir)
    cx, cy, cz = spec.C
    t0, t1 = float(spec.t0), float(spec.t1)

    pts: List[Tuple[float, float]] = []
    N = max(4, segments)
    for i in range(N + 1):
        t = t0 + (t1 - t0) * (i / N)
        x = t
        y = (t*t) / (2.0 * spec.focal)
        px = cx + x*U[0] + y*V[0]
        py = cy + x*U[1] + y*V[1]
        pz = cz + x*U[2] + y*V[2]
        pts.append(iso_project_point(px, py, pz))

    for i in range(len(pts) - 1):
        _add_edge_2d_safe(comp, pts[i], pts[i+1])
    return comp


def iso_step_from_hyperbola(spec: HyperbolaSpec, segments: int = 96):
    """
    ISO hyperbola on Z=0 (polyline), canonical param in the plane (U=xdir^, V=n×U):
        P(t) = C + (a cosh t) U + (b sinh t) V,  t ∈ [t0, t1]
    """
    comp = _make_compound()
    if spec.a <= 0.0 or spec.b <= 0.0:
        return comp

    U, V = _robust_uv_from_plane(spec.n, spec.xdir)
    cx, cy, cz = spec.C
    t0, t1 = float(spec.t0), float(spec.t1)

    pts: List[Tuple[float, float]] = []
    N = max(4, segments)
    for i in range(N + 1):
        t = t0 + (t1 - t0) * (i / N)
        x = spec.a * math.cosh(t)
        y = spec.b * math.sinh(t)
        px = cx + x*U[0] + y*V[0]
