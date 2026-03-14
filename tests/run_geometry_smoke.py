# tests/run_geometry_smoke.py
# Smoke tests: LINE, CIRCLE, ARC, ELLIPSE, ELLIPTIC ARC, BSPLINE, PARABOLA, HYPERBOLA
# - ORTHO (3D) → STEP
# - ISO (2D on Z=0) → STEP (polyline only; no analytic modules required)

import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# ---- Contracts ----
from OPE_IsoGen.Geometry.Contracts.line_spec import LineSpec
from OPE_IsoGen.Geometry.Contracts.circle_spec import CircleSpec
from OPE_IsoGen.Geometry.Contracts.arc_spec import ArcSpec
from OPE_IsoGen.Geometry.Contracts.ellipse_spec import EllipseSpec, EllipticArcSpec
from OPE_IsoGen.Geometry.Contracts.bspline_spec import BSplineSpec
from OPE_IsoGen.Geometry.Contracts.parabola_spec import ParabolaSpec
from OPE_IsoGen.Geometry.Contracts.hyperbola_spec import HyperbolaSpec

# ---- ORTHO (3D) builders ----
from OPE_IsoGen.Geometry.Primitives3D.line3d import make_line
from OPE_IsoGen.Geometry.Primitives3D.circle3d import make_circle_center_normal_radius
from OPE_IsoGen.Geometry.Primitives3D.arc3d import make_arc_center_normal_radius
from OPE_IsoGen.Geometry.Primitives3D.ellipse3d import make_ellipse, make_elliptic_arc
from OPE_IsoGen.Geometry.Primitives3D.bspline3d import make_bspline
from OPE_IsoGen.Geometry.Primitives3D.conics3d import make_parabola, make_hyperbola

# ---- ISO (Z=0 STEP) builders — POLYLINE ONLY ----
from OPE_IsoGen.Geometry.Iso.iso_step_builder import (
    iso_step_from_line,
    iso_step_from_circle,
    iso_step_from_arc,
    iso_step_from_ellipse,
    iso_step_from_elliptic_arc,
    iso_step_from_bspline,
    iso_step_from_parabola,
    iso_step_from_hyperbola,
)


# ---- ISO (DXF) writers — POLYLINE ----
from OPE_IsoGen.Geometry.Iso.iso_dxf_builder import (
    iso_dxf_from_line,
    iso_dxf_from_circle,
    iso_dxf_from_arc,
    iso_dxf_from_ellipse,
    iso_dxf_from_elliptic_arc,
    iso_dxf_from_bspline,
    iso_dxf_from_parabola,
    iso_dxf_from_hyperbola,
)

# ---- ISO (SVG) writers — POLYLINE ----
from OPE_IsoGen.Geometry.Iso.iso_svg_builder import (
    iso_svg_from_line,
    iso_svg_from_circle,
    iso_svg_from_arc,
    iso_svg_from_ellipse,
    iso_svg_from_elliptic_arc,
    iso_svg_from_bspline,
    iso_svg_from_parabola,
    iso_svg_from_hyperbola,
)


from OPE_IsoGen.occt_core.exporters import export_step


def _ensure_out(outdir: str):
    os.makedirs(outdir, exist_ok=True)


def run_ortho(outdir="out/tests"):
    _ensure_out(outdir)

    # -------- LINE (X, Y, Z, diagonal) --------
    lines = [
        ("line_x", LineSpec((0,0,0),(1000,0,0))),
        ("line_y", LineSpec((0,0,0),(0,1000,0))),
        ("line_z", LineSpec((0,0,0),(0,0,1000))),
        ("line_diag", LineSpec((0,0,0),(700,500,300))),
    ]
    for name, spec in lines:
        export_step(make_line(spec), os.path.join(outdir, f"{name}.step"))

    # -------- CIRCLE (XY, YZ, ZX, arbitrary normal) --------
    circles = [
        ("circ_xy",  CircleSpec((0,0,0),(0,0,1),250)),
        ("circ_yz",  CircleSpec((1500,0,0),(1,0,0),220)),
        ("circ_zx",  CircleSpec((0,1500,0),(0,1,0),200)),
        ("circ_any", CircleSpec((500,500,200),(1,1,1),220)),
    ]
    for name, spec in circles:
        export_step(make_circle_center_normal_radius(spec), os.path.join(outdir, f"{name}.step"))

    # -------- ARC (XY, YZ, ZX, arbitrary normal) --------
    arcs = [
        ("arc_xy",  ArcSpec((0,0,0),(0,0,1),250, 0, 90)),
        ("arc_yz",  ArcSpec((1500,0,0),(1,0,0),220, 15, 165)),
        ("arc_zx",  ArcSpec((0,1500,0),(0,1,0),200, 45, 270)),
        ("arc_any", ArcSpec((500,500,200),(1,1,1),200, 30, 210)),
    ]
    for name, spec in arcs:
        export_step(make_arc_center_normal_radius(spec), os.path.join(outdir, f"{name}.step"))

    # -------- ELLIPSE / ELLIPTIC ARC (3D) --------
    ellipses = [
        ("ellipse_xy",  EllipseSpec((0,0,0),(0,0,1),(1,0,0), 300, 180)),
        ("ellipse_yz",  EllipseSpec((1800,0,0),(1,0,0),(0,1,0), 260, 140)),
        ("ellipse_zx",  EllipseSpec((0,1800,0),(0,1,0),(1,0,0), 220, 120)),
        ("ellipse_any", EllipseSpec((600,600,300),(1,1,1),(1,0,1), 240, 100)),
    ]
    for name, spec in ellipses:
        export_step(make_ellipse(spec), os.path.join(outdir, f"{name}.step"))

    e_arcs = [
        ("ellarc_xy",  EllipticArcSpec((0,0,0),(0,0,1),(1,0,0), 300, 180,  0, 120)),
        ("ellarc_yz",  EllipticArcSpec((1800,0,0),(1,0,0),(0,1,0), 260, 140, 30, 210)),
        ("ellarc_zx",  EllipticArcSpec((0,1800,0),(0,1,0),(1,0,0), 220, 120, 45, 270)),
        ("ellarc_any", EllipticArcSpec((600,600,300),(1,1,1),(1,0,1), 240, 100, 10, 170)),
    ]
    for name, spec in e_arcs:
        export_step(make_elliptic_arc(spec), os.path.join(outdir, f"{name}.step"))

    # -------- BSPLINE (3D) --------
    # Use a valid clamped knot vector: sum(mults) = N + p + 1
    bs = BSplineSpec(
        poles=[(0,0,0),(300,150,80),(600,0,0),(900,-150,120),(1200,0,0)],
        knots=[0.0, 0.5, 1.0],    # distinct knot values
        mults=[3, 2, 3],          # 3 (start) + 2 (internal) + 3 (end) = 8 = N(5)+p(2)+1
        degree=2,
        weights=None,
        periodic=False
    )
    export_step(make_bspline(bs), os.path.join(outdir, "bspline.step"))

    # -------- CONICS (3D) --------
    p_specs = [
        ("parab_xy", ParabolaSpec((0,0,0),(0,0,1),(1,0,0), 60, -3, 3)),
        ("parab_yz", ParabolaSpec((2000,0,0),(1,0,0),(0,1,0), 50, -2.5, 2.5)),
    ]
    for name, spec in p_specs:
        export_step(make_parabola(spec), os.path.join(outdir, f"{name}.step"))

    h_specs = [
        ("hyper_xy", HyperbolaSpec((0,0,0),(0,0,1),(1,0,0), 150, 80, -1.2, 1.2)),
        ("hyper_yz", HyperbolaSpec((2000,0,0),(1,0,0),(0,1,0), 130, 70, -1.0, 1.0)),
    ]
    for name, spec in h_specs:
        export_step(make_hyperbola(spec), os.path.join(outdir, f"{name}.step"))

    print("[OK] ORTHO smoke: wrote STEP files in", outdir)


def run_iso_step(outdir="out/tests"):
    _ensure_out(outdir)

    # -------- LINE (X, Y, Z, diagonal) --------
    for name, spec in [
        ("iso_line_x", LineSpec((0,0,0),(1000,0,0))),
        ("iso_line_y", LineSpec((0,0,0),(0,1000,0))),
        ("iso_line_z", LineSpec((0,0,0),(0,0,1000))),
        ("iso_line_diag", LineSpec((0,0,0),(700,500,300))),
    ]:
        export_step(iso_step_from_line(spec), os.path.join(outdir, f"{name}.step"))

    # -------- CIRCLE (XY, YZ, ZX, arbitrary) — polyline ISO --------
    for name, spec in [
        ("iso_circ_xy_poly",  CircleSpec((0,0,0),(0,0,1),250)),
        ("iso_circ_yz_poly",  CircleSpec((1500,0,0),(1,0,0),220)),
        ("iso_circ_zx_poly",  CircleSpec((0,1500,0),(0,1,0),200)),
        ("iso_circ_any_poly", CircleSpec((500,500,200),(1,1,1),220)),
    ]:
        export_step(iso_step_from_circle(spec, chord_tol_mm=5.0), os.path.join(outdir, f"{name}.step"))

    # -------- ARC (XY, YZ, ZX, arbitrary) — polyline ISO --------
    for name, spec in [
        ("iso_arc_xy_poly",  ArcSpec((0,0,0),(0,0,1),250, 0, 90)),
        ("iso_arc_yz_poly",  ArcSpec((1500,0,0),(1,0,0),220, 15, 165)),
        ("iso_arc_zx_poly",  ArcSpec((0,1500,0),(0,1,0),200, 45, 270)),
        ("iso_arc_any_poly", ArcSpec((500,500,200),(1,1,1),200, 30, 210)),
    ]:
        export_step(iso_step_from_arc(spec, chord_tol_mm=5.0), os.path.join(outdir, f"{name}.step"))

    # -------- ELLIPSE / ELLIPTIC ARC (general) — polyline ISO --------
    ellipses = [
        ("iso_ellipse_xy_poly",  EllipseSpec((0,0,0),(0,0,1),(1,0,0), 300, 180)),
        ("iso_ellipse_yz_poly",  EllipseSpec((1800,0,0),(1,0,0),(0,1,0), 260, 140)),
        ("iso_ellipse_zx_poly",  EllipseSpec((0,1800,0),(0,1,0),(1,0,0), 220, 120)),
        ("iso_ellipse_any_poly", EllipseSpec((600,600,300),(1,1,1),(1,0,1), 240, 100)),
    ]
    for name, spec in ellipses:
        export_step(iso_step_from_ellipse(spec, segments=96), os.path.join(outdir, f"{name}.step"))

    e_arcs = [
        ("iso_ellarc_xy_poly",  EllipticArcSpec((0,0,0),(0,0,1),(1,0,0), 300, 180,  0, 120)),
        ("iso_ellarc_yz_poly",  EllipticArcSpec((1800,0,0),(1,0,0),(0,1,0), 260, 140, 30, 210)),
        ("iso_ellarc_zx_poly",  EllipticArcSpec((0,1800,0),(0,1,0),(1,0,0), 220, 120, 45, 270)),
        ("iso_ellarc_any_poly", EllipticArcSpec((600,600,300),(1,1,1),(1,0,1), 240, 100, 10, 170)),
    ]
    for name, spec in e_arcs:
        export_step(iso_step_from_elliptic_arc(spec, segments=64), os.path.join(outdir, f"{name}.step"))

    # -------- BSPLINE / NURBS (polyline ISO: connects projected poles) --------
    bs = BSplineSpec(
        poles=[(0,0,0),(300,150,80),(600,0,0),(900,-150,120),(1200,0,0)],
        knots=[0.0, 0.5, 1.0],
        mults=[3, 2, 3],
        degree=2,
        weights=None,
        periodic=False
    )
    export_step(iso_step_from_bspline(bs), os.path.join(outdir, "iso_bspline.step"))

    # -------- CONICS (parabola/hyperbola) — polyline ISO --------
    export_step(
        iso_step_from_parabola(ParabolaSpec((0,0,0),(0,0,1),(1,0,0), 60, -3, 3)),
        os.path.join(outdir, "iso_parab_xy.step"),
    )
    export_step(
        iso_step_from_parabola(ParabolaSpec((2000,0,0),(1,0,0),(0,1,0), 50, -2.5, 2.5)),
        os.path.join(outdir, "iso_parab_yz.step"),
    )
    export_step(
        iso_step_from_hyperbola(HyperbolaSpec((0,0,0),(0,0,1),(1,0,0), 150, 80, -1.2, 1.2)),
        os.path.join(outdir, "iso_hyper_xy.step"),
    )
    export_step(
        iso_step_from_hyperbola(HyperbolaSpec((2000,0,0),(1,0,0),(0,1,0), 130, 70, -1.0, 1.0)),
        os.path.join(outdir, "iso_hyper_yz.step"),
    )

    print("[OK] ISO STEP (polyline) written to", outdir)


# ---------------- ISO (2D on Z=0) → DXF (polyline) ----------------
def run_iso_dxf(outdir="out/tests_dxf"):
    os.makedirs(outdir, exist_ok=True)

    # ---- LINE (X, Y, Z, diagonal) ----
    for name, spec in [
        ("iso_line_x",   LineSpec((0,0,0),(1000,0,0))),
        ("iso_line_y",   LineSpec((0,0,0),(0,1000,0))),
        ("iso_line_z",   LineSpec((0,0,0),(0,0,1000))),
        ("iso_line_diag",LineSpec((0,0,0),(700,500,300))),
    ]:
        iso_dxf_from_line(spec, os.path.join(outdir, f"{name}.dxf"))

    # ---- CIRCLE (XY, YZ, ZX, arbitrary) — polyline ISO ----
    for name, spec in [
        ("iso_circ_xy_poly",  CircleSpec((0,0,0),(0,0,1),250)),
        ("iso_circ_yz_poly",  CircleSpec((1500,0,0),(1,0,0),220)),
        ("iso_circ_zx_poly",  CircleSpec((0,1500,0),(0,1,0),200)),
        ("iso_circ_any_poly", CircleSpec((500,500,200),(1,1,1),220)),
    ]:
        iso_dxf_from_circle(spec, os.path.join(outdir, f"{name}.dxf"), chord_tol_mm=5.0)

    # ---- ARC (XY, YZ, ZX, arbitrary) — polyline ISO ----
    for name, spec in [
        ("iso_arc_xy_poly",  ArcSpec((0,0,0),(0,0,1),250, 0, 90)),
        ("iso_arc_yz_poly",  ArcSpec((1500,0,0),(1,0,0),220, 15, 165)),
        ("iso_arc_zx_poly",  ArcSpec((0,1500,0),(0,1,0),200, 45, 270)),
        ("iso_arc_any_poly", ArcSpec((500,500,200),(1,1,1),200, 30, 210)),
    ]:
        iso_dxf_from_arc(spec, os.path.join(outdir, f"{name}.dxf"), chord_tol_mm=5.0)

    # ---- ELLIPSE / ELLIPTIC ARC (general) — polyline ISO ----
    ellipses = [
        ("iso_ellipse_xy_poly",  EllipseSpec((0,0,0),(0,0,1),(1,0,0), 300, 180)),
        ("iso_ellipse_yz_poly",  EllipseSpec((1800,0,0),(1,0,0),(0,1,0), 260, 140)),
        ("iso_ellipse_zx_poly",  EllipseSpec((0,1800,0),(0,1,0),(1,0,0), 220, 120)),
        ("iso_ellipse_any_poly", EllipseSpec((600,600,300),(1,1,1),(1,0,1), 240, 100)),
    ]
    for name, spec in ellipses:
        iso_dxf_from_ellipse(spec, os.path.join(outdir, f"{name}.dxf"), segments=96)

    e_arcs = [
        ("iso_ellarc_xy_poly",  EllipticArcSpec((0,0,0),(0,0,1),(1,0,0), 300, 180,  0, 120)),
        ("iso_ellarc_yz_poly",  EllipticArcSpec((1800,0,0),(1,0,0),(0,1,0), 260, 140, 30, 210)),
        ("iso_ellarc_zx_poly",  EllipticArcSpec((0,1800,0),(0,1,0),(1,0,0), 220, 120, 45, 270)),
        ("iso_ellarc_any_poly", EllipticArcSpec((600,600,300),(1,1,1),(1,0,1), 240, 100, 10, 170)),
    ]
    for name, spec in e_arcs:
        iso_dxf_from_elliptic_arc(spec, os.path.join(outdir, f"{name}.dxf"), segments=64)

    # ---- BSPLINE / NURBS (polyline ISO: connects projected poles) ----
    bs = BSplineSpec(
        poles=[(0,0,0),(300,150,80),(600,0,0),(900,-150,120),(1200,0,0)],
        knots=[0.0, 0.5, 1.0],
        mults=[3, 2, 3],
        degree=2,
        weights=None,
        periodic=False
    )
    iso_dxf_from_bspline(bs, os.path.join(outdir, "iso_bspline.dxf"))

    # ---- CONICS (parabola/hyperbola) — polyline ISO ----
    iso_dxf_from_parabola(
        ParabolaSpec((0,0,0),(0,0,1),(1,0,0), 60, -3, 3),
        os.path.join(outdir, "iso_parab_xy.dxf"),
    )
    iso_dxf_from_parabola(
        ParabolaSpec((2000,0,0),(1,0,0),(0,1,0), 50, -2.5, 2.5),
        os.path.join(outdir, "iso_parab_yz.dxf"),
    )
    iso_dxf_from_hyperbola(
        HyperbolaSpec((0,0,0),(0,0,1),(1,0,0), 150, 80, -1.2, 1.2),
        os.path.join(outdir, "iso_hyper_xy.dxf"),
    )
    iso_dxf_from_hyperbola(
        HyperbolaSpec((2000,0,0),(1,0,0),(0,1,0), 130, 70, -1.0, 1.0),
        os.path.join(outdir, "iso_hyper_yz.dxf"),
    )

    print("[OK] ISO DXF (polyline) written to", outdir)

# ---------------- ISO (2D on Z=0) → SVG (polyline) ----------------
def run_iso_svg(outdir="out/tests_svg"):
    os.makedirs(outdir, exist_ok=True)

    # ---- LINE (X, Y, Z, diagonal) ----
    for name, spec in [
        ("iso_line_x",   LineSpec((0,0,0),(1000,0,0))),
        ("iso_line_y",   LineSpec((0,0,0),(0,1000,0))),
        ("iso_line_z",   LineSpec((0,0,0),(0,0,1000))),
        ("iso_line_diag",LineSpec((0,0,0),(700,500,300))),
    ]:
        iso_svg_from_line(spec, os.path.join(outdir, f"{name}.svg"))

    # ---- CIRCLE (XY, YZ, ZX, arbitrary) — polyline ISO ----
    for name, spec in [
        ("iso_circ_xy_poly",  CircleSpec((0,0,0),(0,0,1),250)),
        ("iso_circ_yz_poly",  CircleSpec((1500,0,0),(1,0,0),220)),
        ("iso_circ_zx_poly",  CircleSpec((0,1500,0),(0,1,0),200)),
        ("iso_circ_any_poly", CircleSpec((500,500,200),(1,1,1),220)),
    ]:
        iso_svg_from_circle(spec, os.path.join(outdir, f"{name}.svg"), chord_tol_mm=5.0)

    # ---- ARC (XY, YZ, ZX, arbitrary) — polyline ISO ----
    for name, spec in [
        ("iso_arc_xy_poly",  ArcSpec((0,0,0),(0,0,1),250, 0, 90)),
        ("iso_arc_yz_poly",  ArcSpec((1500,0,0),(1,0,0),220, 15, 165)),
        ("iso_arc_zx_poly",  ArcSpec((0,1500,0),(0,1,0),200, 45, 270)),
        ("iso_arc_any_poly", ArcSpec((500,500,200),(1,1,1),200, 30, 210)),
    ]:
        iso_svg_from_arc(spec, os.path.join(outdir, f"{name}.svg"), chord_tol_mm=5.0)

    # ---- ELLIPSE / ELLIPTIC ARC (general) — polyline ISO ----
    ellipses = [
        ("iso_ellipse_xy_poly",  EllipseSpec((0,0,0),(0,0,1),(1,0,0), 300, 180)),
        ("iso_ellipse_yz_poly",  EllipseSpec((1800,0,0),(1,0,0),(0,1,0), 260, 140)),
        ("iso_ellipse_zx_poly",  EllipseSpec((0,1800,0),(0,1,0),(1,0,0), 220, 120)),
        ("iso_ellipse_any_poly", EllipseSpec((600,600,300),(1,1,1),(1,0,1), 240, 100)),
    ]
    for name, spec in ellipses:
        iso_svg_from_ellipse(spec, os.path.join(outdir, f"{name}.svg"), segments=96)

    e_arcs = [
        ("iso_ellarc_xy_poly",  EllipticArcSpec((0,0,0),(0,0,1),(1,0,0), 300, 180,  0, 120)),
        ("iso_ellarc_yz_poly",  EllipticArcSpec((1800,0,0),(1,0,0),(0,1,0), 260, 140, 30, 210)),
        ("iso_ellarc_zx_poly",  EllipticArcSpec((0,1800,0),(0,1,0),(1,0,0), 220, 120, 45, 270)),
        ("iso_ellarc_any_poly", EllipticArcSpec((600,600,300),(1,1,1),(1,0,1), 240, 100, 10, 170)),
    ]
    for name, spec in e_arcs:
        iso_svg_from_elliptic_arc(spec, os.path.join(outdir, f"{name}.svg"), segments=64)

    # ---- BSPLINE / NURBS (polyline ISO: connects projected poles) ----
    bs = BSplineSpec(
        poles=[(0,0,0),(300,150,80),(600,0,0),(900,-150,120),(1200,0,0)],
        knots=[0.0, 0.5, 1.0],
        mults=[3, 2, 3],
        degree=2,
        weights=None,
        periodic=False
    )
    iso_svg_from_bspline(bs, os.path.join(outdir, "iso_bspline.svg"))

    # ---- CONICS (parabola/hyperbola) — polyline ISO ----
    iso_svg_from_parabola(
        ParabolaSpec((0,0,0),(0,0,1),(1,0,0), 60, -3, 3),
        os.path.join(outdir, "iso_parab_xy.svg"),
    )
    iso_svg_from_parabola(
        ParabolaSpec((2000,0,0),(1,0,0),(0,1,0), 50, -2.5, 2.5),
        os.path.join(outdir, "iso_parab_yz.svg"),
    )
    iso_svg_from_hyperbola(
        HyperbolaSpec((0,0,0),(0,0,1),(1,0,0), 150, 80, -1.2, 1.2),
        os.path.join(outdir, "iso_hyper_xy.svg"),
    )
    iso_svg_from_hyperbola(
        HyperbolaSpec((2000,0,0),(1,0,0),(0,1,0), 130, 70, -1.0, 1.0),
        os.path.join(outdir, "iso_hyper_yz.svg"),
    )

    print("[OK] ISO SVG (polyline) written to", outdir)

def run_iso(outdir: str = "out/tests") -> None:
    run_iso_step(outdir)
    run_iso_dxf(outdir)
    run_iso_svg(outdir)

if __name__ == "__main__":
    # Default: run both
    run_ortho()
    run_iso()