from __future__ import annotations
import math
from typing import List, Tuple
from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopoDS import TopoDS_Compound
from .projector_top import iso_project_point
from ..Contracts.line_spec import LineSpec
from ..Contracts.circle_spec import CircleSpec
from ..Contracts.arc_spec import ArcSpec
from .circle_iso import _basis_from_normal, _nseg_for_chord_tol  # reuse sampling helpers

def _add_edge_2d(comp: TopoDS_Compound, a2: Tuple[float,float], b2: Tuple[float,float]):
    mk = BRepBuilderAPI_MakeEdge(gp_Pnt(a2[0], a2[1], 0.0), gp_Pnt(b2[0], b2[1], 0.0))
    BRep_Builder().Add(comp, mk.Edge())

def iso_step_from_line(spec: LineSpec):
    """Return a TopoDS_Compound with one 2D edge (Z=0) for isometric line."""
    comp = TopoDS_Compound(); BRep_Builder().MakeCompound(comp)
    a2 = iso_project_point(*spec.S)
    b2 = iso_project_point(*spec.E)
    _add_edge_2d(comp, a2, b2)
    return comp

def iso_step_from_circle(spec: CircleSpec, chord_tol_mm: float = 1.0):
    """Return 2D circle as polyline edges (ellipse) in Z=0 STEP."""
    comp = TopoDS_Compound(); b = BRep_Builder(); b.MakeCompound(comp)
    if spec.R <= 0: return comp
    u, v = _basis_from_normal(spec.n)
    nseg = _nseg_for_chord_tol(spec.R, chord_tol_mm)
    pts2: List[Tuple[float,float]] = []
    cx, cy, cz = spec.C
    for i in range(nseg+1):
        t = 2*math.pi * i / nseg
        px = cx + spec.R*(u[0]*math.cos(t) + v[0]*math.sin(t))
        py = cy + spec.R*(u[1]*math.cos(t) + v[1]*math.sin(t))
        pz = cz + spec.R*(u[2]*math.cos(t) + v[2]*math.sin(t))
        pts2.append(iso_project_point(px, py, pz))
    # stitch segments
    for i in range(nseg):
        _add_edge_2d(comp, pts2[i], pts2[i+1])
    return comp

def iso_step_from_arc(spec: ArcSpec, chord_tol_mm: float = 1.0):
    """Return 2D arc as polyline edges (ellipse segment) in Z=0 STEP."""
    comp = TopoDS_Compound(); b = BRep_Builder(); b.MakeCompound(comp)
    if spec.R <= 0: return comp
    u, v = _basis_from_normal(spec.n)
    a0 = math.radians(spec.a0_deg); a1 = math.radians(spec.a1_deg)
    sweep = a1 - a0
    arc_len = abs(sweep)*spec.R
    nseg = max(4, int(max(1.0, arc_len / max(1e-6, chord_tol_mm))))
    pts2: List[Tuple[float,float]] = []
    cx, cy, cz = spec.C
    for i in range(nseg+1):
        t = a0 + sweep*(i/nseg)
        px = cx + spec.R*(u[0]*math.cos(t) + v[0]*math.sin(t))
        py = cy + spec.R*(u[1]*math.cos(t) + v[1]*math.sin(t))
        pz = cz + spec.R*(u[2]*math.cos(t) + v[2]*math.sin(t))
        pts2.append(iso_project_point(px, py, pz))
    for i in range(nseg):
        _add_edge_2d(comp, pts2[i], pts2[i+1])
    return comp