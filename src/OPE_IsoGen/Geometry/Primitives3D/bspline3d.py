from __future__ import annotations
from OCC.Core.gp import gp_Pnt
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.TColStd import TColStd_Array1OfReal, TColStd_Array1OfInteger
from OCC.Core.Geom import Geom_BSplineCurve
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from ..Contracts.bspline_spec import BSplineSpec

def _arr_poles3d(poles):
    arr = TColgp_Array1OfPnt(1, len(poles))
    for i,(x,y,z) in enumerate(poles, start=1):
        arr.SetValue(i, gp_Pnt(float(x), float(y), float(z)))
    return arr

def _arr_reals(vals):
    arr = TColStd_Array1OfReal(1, len(vals))
    for i,v in enumerate(vals, start=1): arr.SetValue(i, float(v))
    return arr

def _arr_ints(vals):
    arr = TColStd_Array1OfInteger(1, len(vals))
    for i,v in enumerate(vals, start=1): arr.SetValue(i, int(v))
    return arr

def make_bspline(spec: BSplineSpec):
    P = _arr_poles3d(spec.poles)
    K = _arr_reals(spec.knots)
    M = _arr_ints(spec.mults)
    if spec.weights:
        W = _arr_reals(spec.weights)
        crv = Geom_BSplineCurve(P, W, K, M, int(spec.degree), bool(spec.periodic))
    else:
        crv = Geom_BSplineCurve(P, K, M, int(spec.degree), bool(spec.periodic))
    return BRepBuilderAPI_MakeEdge(crv).Edge()