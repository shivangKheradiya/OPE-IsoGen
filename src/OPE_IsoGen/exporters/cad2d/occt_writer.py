"""
Optional OCCT-based 2D CAD exporter (DXF/STEP/IGES).
Requires 'pythonocc-core' in the active environment.
"""
try:
    from OCC.Core.gp import gp_Pnt2d
    HAVE_OCC = True
except Exception:
    HAVE_OCC = False

def export_to_dxf_2d(_prims, _path: str):
    if not HAVE_OCC:
        raise RuntimeError("pythonocc-core not available; install optional 'cad' extra or use conda env.")
    # TODO: map Line2D and Polyline2D to OCC 2D geometry and write DXF
    raise NotImplementedError("DXF export not implemented yet.")
