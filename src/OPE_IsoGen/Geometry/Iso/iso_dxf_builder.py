# src/OPE_IsoGen/Geometry/Iso/iso_dxf_builder.py
from __future__ import annotations
import math, os
from typing import List, Tuple

try:
    import ezdxf
except Exception as e:
    ezdxf = None

from .projector_top import iso_project_point
from ..Contracts.line_spec import LineSpec
from ..Contracts.circle_spec import CircleSpec
from ..Contracts.arc_spec import ArcSpec
from ..Contracts.ellipse_spec import EllipseSpec, EllipticArcSpec
from ..Contracts.bspline_spec import BSplineSpec
from ..Contracts.parabola_spec import ParabolaSpec
from ..Contracts.hyperbola_spec import HyperbolaSpec

# Reuse circle helpers (sampling)
from .circle_iso import _basis_from_normal, _nseg_for_chord_tol

# ---------- small helpers ----------
def _need_ezdxf():
    if ezdxf is None:
        raise ImportError("DXF export requires 'ezdxf'. Install with: pip install ezdxf")

# --- add near the top (after imports) ---
def _set_dxf_units_mm(doc):
    """
    Set DXF modelspace units to millimetres, compatible across ezdxf versions.
    - Prefer doc.units (if available)
    - Always set $INSUNITS (AutoCAD header: 4 = mm) and $MEASUREMENT (1 = metric)
    - Add $LUNITS/$LUPREC if not present (viewer UI formatting only)
    """
    # 1) Preferred API where available
    try:
        import ezdxf
        # ezdxf.units.MM exists on modern versions
        doc.units = ezdxf.units.MM
    except Exception:
        pass

    # 2) Header variables (works broadly)
    hdr = doc.header

    # $INSUNITS: 4 = millimetres
    try:
        import ezdxf
        hdr["$INSUNITS"] = getattr(ezdxf.units, "MM", 4)
    except Exception:
        hdr["$INSUNITS"] = 4  # mm

    # $MEASUREMENT: 1 = metric (0 = English)
    hdr["$MEASUREMENT"] = 1

    # $LUNITS (2 = decimal) — if missing, add it
    if "$LUNITS" not in hdr:
        try:
            hdr.add_var("$LUNITS", 2)
        except Exception:
            hdr["$LUNITS"] = 2

    # $LUPREC (linear precision = 4) — if missing, add it
    if "$LUPREC" not in hdr:
        try:
            hdr.add_var("$LUPREC", 4)
        except Exception:
            hdr["$LUPREC"] = 4

def _unit3(v: Tuple[float,float,float]) -> Tuple[float,float,float]:
    L = math.sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2]) or 1.0
    return (v[0]/L, v[1]/L, v[2]/L)

def _cross(a: Tuple[float,float,float], b: Tuple[float,float,float]) -> Tuple[float,float,float]:
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])

def _robust_uv_from_plane(n: Tuple[float,float,float],
                          xdir_hint: Tuple[float,float,float] | None = None):
    n_u = _unit3(n)
    if xdir_hint is not None:
        U = _unit3(xdir_hint)
        V = _cross(n_u, U)
        if abs(V[0])+abs(V[1])+abs(V[2]) < 1e-12:
            ref = (1.0,0.0,0.0) if abs(n_u[0])<0.9 else (0.0,1.0,0.0)
            U = _unit3(_cross(ref, n_u))
            V = _cross(n_u, U)
    else:
        ref = (1.0,0.0,0.0) if abs(n_u[0])<0.9 else (0.0,1.0,0.0)
        U = _unit3(_cross(ref, n_u))
        V = _cross(n_u, U)
    return U, _unit3(V)

def _save_doc(doc, path: str):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    doc.saveas(path)

# ---------- per-geometry writers (one file per geometry, matching your STEP pattern) ----------
def iso_dxf_from_line(spec: LineSpec, path: str, layer: str = "ISO"):
    _need_ezdxf()
    doc = ezdxf.new(setup=True); _set_dxf_units_mm(doc)
    msp = doc.modelspace() 
    a2 = iso_project_point(*spec.S); b2 = iso_project_point(*spec.E)
    msp.add_line((a2[0], a2[1], 0.0), (b2[0], b2[1], 0.0), dxfattribs={"layer": layer})
    _save_doc(doc, path)

def iso_dxf_from_circle(spec: CircleSpec, path: str, chord_tol_mm: float = 1.0, layer: str = "ISO"):
    _need_ezdxf()
    doc = ezdxf.new(setup=True); _set_dxf_units_mm(doc)
    msp = doc.modelspace()
    if spec.R <= 0: _save_doc(doc, path); return
    u, v = _basis_from_normal(spec.n)
    nseg = _nseg_for_chord_tol(spec.R, chord_tol_mm)
    cx, cy, cz = spec.C
    pts: List[Tuple[float,float]] = []
    for i in range(nseg+1):
        t = 2*math.pi*i/nseg
        px = cx + spec.R*(u[0]*math.cos(t) + v[0]*math.sin(t))
        py = cy + spec.R*(u[1]*math.cos(t) + v[1]*math.sin(t))
        pz = cz + spec.R*(u[2]*math.cos(t) + v[2]*math.sin(t))
        pts.append(iso_project_point(px,py,pz))
    msp.add_lwpolyline(pts, dxfattribs={"layer": layer, "closed": True})
    _save_doc(doc, path)

def iso_dxf_from_arc(spec: ArcSpec, path: str, chord_tol_mm: float = 1.0, layer: str = "ISO"):
    _need_ezdxf()
    doc = ezdxf.new(setup=True); _set_dxf_units_mm(doc)
    msp = doc.modelspace()
    if spec.R <= 0: _save_doc(doc, path); return
    u, v = _basis_from_normal(spec.n)
    a0 = math.radians(spec.a0_deg); a1 = math.radians(spec.a1_deg)
    sweep = a1 - a0
    arc_len = abs(sweep) * spec.R
    nseg = max(4, int(max(1.0, arc_len / max(1e-6, chord_tol_mm))))
    cx, cy, cz = spec.C
    pts: List[Tuple[float,float]] = []
    for i in range(nseg+1):
        t = a0 + sweep*(i/nseg)
        px = cx + spec.R*(u[0]*math.cos(t) + v[0]*math.sin(t))
        py = cy + spec.R*(u[1]*math.cos(t) + v[1]*math.sin(t))
        pz = cz + spec.R*(u[2]*math.cos(t) + v[2]*math.sin(t))
        pts.append(iso_project_point(px,py,pz))
    msp.add_lwpolyline(pts, dxfattribs={"layer": layer, "closed": False})
    _save_doc(doc, path)

def iso_dxf_from_ellipse(spec: EllipseSpec, path: str, segments: int = 96, layer: str = "ISO"):
    _need_ezdxf()
    doc = ezdxf.new(setup=True); _set_dxf_units_mm(doc)
    msp = doc.modelspace()
    if spec.a <= 0 or spec.b <= 0: _save_doc(doc, path); return
    U, V = _robust_uv_from_plane(spec.n, spec.xdir)
    cx, cy, cz = spec.C
    pts: List[Tuple[float,float]] = []
    N = max(8, segments)
    for i in range(N+1):
        t = 2.0*math.pi*i/N
        px = cx + spec.a*(U[0]*math.cos(t)) + spec.b*(V[0]*math.sin(t))
        py = cy + spec.a*(U[1]*math.cos(t)) + spec.b*(V[1]*math.sin(t))
        pz = cz + spec.a*(U[2]*math.cos(t)) + spec.b*(V[2]*math.sin(t))
        pts.append(iso_project_point(px,py,pz))
    msp.add_lwpolyline(pts, dxfattribs={"layer": layer, "closed": True})
    _save_doc(doc, path)

def iso_dxf_from_elliptic_arc(spec: EllipticArcSpec, path: str, segments: int = 64, layer: str = "ISO"):
    _need_ezdxf()
    doc = ezdxf.new(setup=True); _set_dxf_units_mm(doc)
    msp = doc.modelspace()
    if spec.a <= 0 or spec.b <= 0: _save_doc(doc, path); return
    U, V = _robust_uv_from_plane(spec.n, spec.xdir)
    cx, cy, cz = spec.C
    a0 = math.radians(spec.start_deg); a1 = math.radians(spec.end_deg)
    pts: List[Tuple[float,float]] = []
    N = max(2, segments)
    for i in range(N+1):
        t = a0 + (a1-a0)*i/N
        px = cx + spec.a*(U[0]*math.cos(t)) + spec.b*(V[0]*math.sin(t))
        py = cy + spec.a*(U[1]*math.cos(t)) + spec.b*(V[1]*math.sin(t))
        pz = cz + spec.a*(U[2]*math.cos(t)) + spec.b*(V[2]*math.sin(t))
        pts.append(iso_project_point(px,py,pz))
    msp.add_lwpolyline(pts, dxfattribs={"layer": layer, "closed": False})
    _save_doc(doc, path)

def iso_dxf_from_bspline(spec: BSplineSpec, path: str, layer: str = "ISO"):
    _need_ezdxf()
    doc = ezdxf.new(setup=True); _set_dxf_units_mm(doc)
    msp = doc.modelspace()
    if not spec.poles or len(spec.poles) < 2: _save_doc(doc, path); return
    pts = [ iso_project_point(*P) for P in spec.poles ]
    msp.add_lwpolyline(pts, dxfattribs={"layer": layer, "closed": False})
    _save_doc(doc, path)

def iso_dxf_from_parabola(spec: ParabolaSpec, path: str, segments: int = 96, layer: str = "ISO"):
    _need_ezdxf()
    doc = ezdxf.new(setup=True); _set_dxf_units_mm(doc)
    msp = doc.modelspace()
    if spec.focal == 0.0: _save_doc(doc, path); return
    U, V = _robust_uv_from_plane(spec.n, spec.xdir)
    cx, cy, cz = spec.C
    t0, t1 = float(spec.t0), float(spec.t1)
    pts: List[Tuple[float,float]] = []
    N = max(4, segments)
    for i in range(N+1):
        t = t0 + (t1-t0)*i/N
        x = t; y = (t*t)/(2.0*spec.focal)
        px = cx + x*U[0] + y*V[0]
        py = cy + x*U[1] + y*V[1]
        pz = cz + x*U[2] + y*V[2]
        pts.append(iso_project_point(px,py,pz))
    msp.add_lwpolyline(pts, dxfattribs={"layer": layer, "closed": False})
    _save_doc(doc, path)

def iso_dxf_from_hyperbola(spec: HyperbolaSpec, path: str, segments: int = 96, layer: str = "ISO"):
    _need_ezdxf()
    doc = ezdxf.new(setup=True); _set_dxf_units_mm(doc)
    msp = doc.modelspace()
    if spec.a <= 0 or spec.b <= 0: _save_doc(doc, path); return
    U, V = _robust_uv_from_plane(spec.n, spec.xdir)
    cx, cy, cz = spec.C
    t0, t1 = float(spec.t0), float(spec.t1)
    pts: List[Tuple[float,float]] = []
    N = max(4, segments)
    for i in range(N+1):
        t = t0 + (t1-t0)*i/N
        x = spec.a*math.cosh(t); y = spec.b*math.sinh(t)
        px = cx + x*U[0] + y*V[0]
        py = cy + x*U[1] + y*V[1]
        pz = cz + x*U[2] + y*V[2]
        pts.append(iso_project_point(px,py,pz))
    msp.add_lwpolyline(pts, dxfattribs={"layer": layer, "closed": False})
    _save_doc(doc, path)