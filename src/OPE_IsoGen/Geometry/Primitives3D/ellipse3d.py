from __future__ import annotations
import math
from OCC.Core.gp import gp_Elips
from OCC.Core.Geom import Geom_Ellipse, Geom_TrimmedCurve
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from ..Contracts.ellipse_spec import EllipseSpec, EllipticArcSpec
from ..Math.gp_helpers import as_pnt, as_vec, unit_vec, plane_ax2

def make_ellipse(spec: EllipseSpec):
    """
    Build 3D ellipse edge (full 0..2π) from (C,n,xdir,a,b).
    """
    ax2 = plane_ax2(spec.C, spec.n, spec.xdir)
    el = gp_Elips(ax2, float(spec.a), float(spec.b))
    gel = Geom_Ellipse(el)
    full = Geom_TrimmedCurve(gel, 0.0, 2*math.pi, True)
    return BRepBuilderAPI_MakeEdge(full).Edge()

def make_elliptic_arc(spec: EllipticArcSpec):
    """
    Build 3D elliptic arc from ellipse spec + (start_deg,end_deg) in ellipse parameter.
    """
    ax2 = plane_ax2(spec.C, spec.n, spec.xdir)
    el = gp_Elips(ax2, float(spec.a), float(spec.b))
    gel = Geom_Ellipse(el)
    arc = Geom_TrimmedCurve(gel, math.radians(spec.start_deg), math.radians(spec.end_deg), True)
    return BRepBuilderAPI_MakeEdge(arc).Edge()