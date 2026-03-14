from __future__ import annotations
from OCC.Core.gp import gp_Parab, gp_Hypr
from OCC.Core.Geom import Geom_Parabola, Geom_Hyperbola, Geom_TrimmedCurve
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from ..Contracts.parabola_spec import ParabolaSpec
from ..Contracts.hyperbola_spec import HyperbolaSpec
from ..Math.gp_helpers import plane_ax2

def make_parabola(spec: ParabolaSpec):
    """
    3D parabola: gp_Parab(Ax2, focal), trimmed by [t0,t1].
    """
    ax2 = plane_ax2(spec.C, spec.n, spec.xdir)
    pb = gp_Parab(ax2, float(spec.focal))
    gp_pb = Geom_Parabola(pb)
    arc = Geom_TrimmedCurve(gp_pb, float(spec.t0), float(spec.t1), True)
    return BRepBuilderAPI_MakeEdge(arc).Edge()

def make_hyperbola(spec: HyperbolaSpec):
    """
    3D hyperbola: gp_Hypr(Ax2, a,b), trimmed by [t0,t1].
    """
    ax2 = plane_ax2(spec.C, spec.n, spec.xdir)
    hb = gp_Hypr(ax2, float(spec.a), float(spec.b))
    gp_hb = Geom_Hyperbola(hb)
    arc = Geom_TrimmedCurve(gp_hb, float(spec.t0), float(spec.t1), True)
    return BRepBuilderAPI_MakeEdge(arc).Edge()