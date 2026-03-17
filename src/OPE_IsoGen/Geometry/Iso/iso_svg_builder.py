# src/OPE_IsoGen/Geometry/Iso/iso_svg_builder.py
from __future__ import annotations
import math, os
from typing import List, Tuple
from .projector_top import iso_project_point
from ..Contracts.line_spec import LineSpec
from ..Contracts.circle_spec import CircleSpec
from ..Contracts.arc_spec import ArcSpec
from ..Contracts.ellipse_spec import EllipseSpec, EllipticArcSpec
from ..Contracts.bspline_spec import BSplineSpec
from ..Contracts.parabola_spec import ParabolaSpec
from ..Contracts.hyperbola_spec import HyperbolaSpec
from .circle_iso import _basis_from_normal, _nseg_for_chord_tol
from OPE_IsoGen.Geometry.Contracts.text_spec import TextSpec
from OPE_IsoGen.Geometry.Iso.projector_top import iso_project_point
from OPE_IsoGen.Geometry.Iso.text_orientation import ISOTextOrientation

def _write_svg_polylines(polylines: List[List[Tuple[float,float]]],
                         lines: List[Tuple[Tuple[float,float],Tuple[float,float]]],
                         path: str, stroke_width: int = 2, padding: float = 20.0):
    # collect bounds
    xs: List[float] = []; ys: List[float] = []
    for a,b in lines:
        xs += [a[0], b[0]]; ys += [a[1], b[1]]
    for pts in polylines:
        for x,y in pts: xs.append(x); ys.append(y)
    if not xs:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w") as f: f.write("<svg/>")
        return
    minx, maxx = min(xs), max(xs); miny, maxy = min(ys), max(ys)
    W = (maxx - minx) + 2*padding
    H = (maxy - miny) + 2*padding
    def tx(x): return (x - minx) + padding
    def ty(y): return H - ((y - miny) + padding)

    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}">\n')
        f.write(f'<g stroke="black" stroke-width="{stroke_width}" fill="none" '
                'stroke-linecap="round" stroke-linejoin="round">\n')
        for a,b in lines:
            f.write(f'<line x1="{tx(a[0]):.2f}" y1="{ty(a[1]):.2f}" '
                    f'x2="{tx(b[0]):.2f}" y2="{ty(b[1]):.2f}"/>\n')
        for pts in polylines:
            if len(pts) >= 2:
                pts_str = " ".join(f"{tx(x):.2f},{ty(y):.2f}" for x,y in pts)
                f.write(f'<polyline points="{pts_str}"/>\n')
        f.write('</g></svg>\n')

def iso_svg_from_line(spec: LineSpec, path: str, stroke_width: int = 2, padding: float = 20.0):
    a2 = iso_project_point(*spec.S); b2 = iso_project_point(*spec.E)
    _write_svg_polylines([], [(a2,b2)], path, stroke_width, padding)

def iso_svg_from_circle(spec: CircleSpec, path: str, chord_tol_mm: float = 1.0,
                        stroke_width: int = 2, padding: float = 20.0):
    if spec.R <= 0:
        _write_svg_polylines([], [], path, stroke_width, padding); return
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
    _write_svg_polylines([pts], [], path, stroke_width, padding)

def iso_svg_from_arc(spec: ArcSpec, path: str, chord_tol_mm: float = 1.0,
                     stroke_width: int = 2, padding: float = 20.0):
    if spec.R <= 0:
        _write_svg_polylines([], [], path, stroke_width, padding); return
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
    _write_svg_polylines([pts], [], path, stroke_width, padding)

def iso_svg_from_ellipse(spec: EllipseSpec, path: str, segments: int = 96,
                         stroke_width: int = 2, padding: float = 20.0):
    if spec.a <= 0 or spec.b <= 0:
        _write_svg_polylines([], [], path, stroke_width, padding); return
    def _unit3(v): 
        L = math.sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2]) or 1.0
        return (v[0]/L, v[1]/L, v[2]/L)
    def _cross(a,b):
        return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
    U = _unit3(spec.xdir); V = _unit3(_cross(spec.n, U))
    cx, cy, cz = spec.C
    pts: List[Tuple[float,float]] = []
    N = max(8, segments)
    for i in range(N+1):
        t = 2.0*math.pi*i/N
        px = cx + spec.a*(U[0]*math.cos(t)) + spec.b*(V[0]*math.sin(t))
        py = cy + spec.a*(U[1]*math.cos(t)) + spec.b*(V[1]*math.sin(t))
        pz = cz + spec.a*(U[2]*math.cos(t)) + spec.b*(V[2]*math.sin(t))
        pts.append(iso_project_point(px,py,pz))
    _write_svg_polylines([pts], [], path, stroke_width, padding)

def iso_svg_from_elliptic_arc(spec: EllipticArcSpec, path: str, segments: int = 64,
                              stroke_width: int = 2, padding: float = 20.0):
    def _unit3(v): 
        L = math.sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2]) or 1.0
        return (v[0]/L, v[1]/L, v[2]/L)
    def _cross(a,b):
        return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
    if spec.a <= 0 or spec.b <= 0:
        _write_svg_polylines([], [], path, stroke_width, padding); return
    U = _unit3(spec.xdir); V = _unit3(_cross(spec.n, U))
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
    _write_svg_polylines([pts], [], path, stroke_width, padding)

def iso_svg_from_bspline(spec: BSplineSpec, path: str, stroke_width: int = 2, padding: float = 20.0):
    if not spec.poles or len(spec.poles) < 2:
        _write_svg_polylines([], [], path, stroke_width, padding); return
    pts = [ iso_project_point(*P) for P in spec.poles ]
    _write_svg_polylines([pts], [], path, stroke_width, padding)

def iso_svg_from_parabola(spec: ParabolaSpec, path: str, segments: int = 96,
                          stroke_width: int = 2, padding: float = 20.0):
    def _unit3(v): 
        L = math.sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2]) or 1.0
        return (v[0]/L, v[1]/L, v[2]/L)
    def _cross(a,b):
        return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
    if spec.focal == 0.0:
        _write_svg_polylines([], [], path, stroke_width, padding); return
    U = _unit3(spec.xdir); V = _unit3(_cross(spec.n, U))
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
    _write_svg_polylines([pts], [], path, stroke_width, padding)

def iso_svg_from_hyperbola(spec: HyperbolaSpec, path: str, segments: int = 96,
                           stroke_width: int = 2, padding: float = 20.0):
    def _unit3(v): 
        L = math.sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2]) or 1.0
        return (v[0]/L, v[1]/L, v[2]/L)
    def _cross(a,b):
        return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
    if spec.a <= 0 or spec.b <= 0:
        _write_svg_polylines([], [], path, stroke_width, padding); return
    U = _unit3(spec.xdir); V = _unit3(_cross(spec.n, U))
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
    _write_svg_polylines([pts], [], path, stroke_width, padding)

def iso_svg_from_text(
    spec: TextSpec,
    path: str,
    stroke_width: int = 2,
    padding: float = 20.0
):
    import math

    # Local helpers exactly like all other iso_svg_* functions:
    def _unit3(v):
        L = math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2]) or 1.0
        return (v[0]/L, v[1]/L, v[2]/L)

    def _cross(a, b):
        return (
            a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0]
        )

    # 1) Build text plane basis (U,V) exactly like hyperbola
    U = _unit3(spec.xdir)
    V = _unit3(_cross(spec.n, U))

    # 2) Project anchor point C into ISO space
    sx, sy = iso_project_point(*spec.C)

    # 3) Compute snapped ISO angle using your ISO orientation class
    from OPE_IsoGen.Geometry.Iso.text_orientation import ISOTextOrientation
    angle = ISOTextOrientation.angle_deg(spec.C, spec.xdir, spec.rot_deg)
    angle_svg = -angle   # SVG rotates opposite direction

    # 4) Determine horizontal anchor for SVG
    anchor = {
        "LEFT": "start",
        "CENTER": "middle",
        "RIGHT": "end",
    }.get(spec.halign.upper(), "start")

    # 5) Build auto-fit bounding box (same as hyperbola path)
    minx = sx - padding
    maxx = sx + padding
    miny = sy - padding
    maxy = sy + padding

    W = maxx - minx
    H = maxy - miny

    def tx(x): return x - minx
    def ty(y): return H - (y - miny)

    # 6) Output SVG
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{W}mm" height="{H}mm" '
            f'viewBox="0 0 {W} {H}">\n'
        )
        f.write('<g fill="black" stroke="none">\n')

        # ONE text element — this is analogous to ONE polyline in hyperbola
        f.write(
            f'<text x="{tx(sx):.3f}" y="{ty(sy):.3f}" '
            f'font-size="{spec.height_mm}mm" '
            f'text-anchor="{anchor}" '
            f'transform="rotate({angle_svg:.3f},{tx(sx):.3f},{ty(sy):.3f})" '
            f'dominant-baseline="alphabetic">'
            f'{spec.text}'
            f'</text>\n'
        )

        f.write('</g></svg>\n')