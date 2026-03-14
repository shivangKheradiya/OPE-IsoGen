# tests/run_geometry_smoke.py
# Simple smoke test for Phase-1: LINE, CIRCLE, ARC
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from OPE_IsoGen.Geometry.Contracts.line_spec import LineSpec
from OPE_IsoGen.Geometry.Contracts.circle_spec import CircleSpec
from OPE_IsoGen.Geometry.Contracts.arc_spec import ArcSpec

# ORTHO (3D) builders
from OPE_IsoGen.Geometry.Primitives3D.line3d import make_line
from OPE_IsoGen.Geometry.Primitives3D.circle3d import make_circle_center_normal_radius
from OPE_IsoGen.Geometry.Primitives3D.arc3d import make_arc_center_normal_radius
from OPE_IsoGen.occt_core.exporters import export_step

# ISO (2D) samplers
from OPE_IsoGen.Geometry.Iso.line_iso import iso_line
from OPE_IsoGen.Geometry.Iso.circle_iso import iso_circle
from OPE_IsoGen.Geometry.Iso.arc_iso import iso_arc
from OPE_IsoGen.Geometry.Iso.iso_step_builder import iso_step_from_line, iso_step_from_circle, iso_step_from_arc


def run_ortho(outdir="out/tests"):
    os.makedirs(outdir, exist_ok=True)
    # LINE
    e_line = make_line(LineSpec((0,0,0), (1000,0,0)))
    export_step(e_line, os.path.join(outdir, "line.step"))
    # CIRCLE
    e_circ = make_circle_center_normal_radius(CircleSpec((0,0,0),(0,0,1),250))
    export_step(e_circ, os.path.join(outdir, "circle.step"))
    # ARC (0..90° in XY)
    e_arc = make_arc_center_normal_radius(ArcSpec((0,0,0),(0,0,1),250, 0, 90))
    export_step(e_arc, os.path.join(outdir, "arc.step"))
    print("[OK] ORTHO smoke: wrote STEP files in", outdir)

def run_iso(outdir="out/tests"):
    os.makedirs(outdir, exist_ok=True)
    # LINE 2D
    a,b = iso_line(LineSpec((0,0,0),(1000,0,0)))
    print("[ISO] line 2D:", a, b)
    # CIRCLE 2D (XY)
    pts = iso_circle(CircleSpec((0,0,0),(0,0,1),250), chord_tol_mm=5.0)
    print("[ISO] circle 2D pts:", len(pts))
    # ARC 2D (0..90° in XY)
    pts2 = iso_arc(ArcSpec((0,0,0),(0,0,1),250, 0, 90), chord_tol_mm=5.0)
    print("[ISO] arc 2D pts:", len(pts2))
    # Optionally dump simple TSV for quick visual inspection
    with open(os.path.join(outdir,"iso_circle.tsv"), "w") as f:
        for x,y in pts: f.write(f"{x}\t{y}\n")
    with open(os.path.join(outdir,"iso_arc.tsv"), "w") as f:
        for x,y in pts2: f.write(f"{x}\t{y}\n")
    print("[OK] ISO smoke: wrote 2D TSVs in", outdir)

def run_iso_step(outdir="out/tests"):
    os.makedirs(outdir, exist_ok=True)
    # LINE
    shape_line = iso_step_from_line(LineSpec((0,0,0),(1000,0,0)))
    export_step(shape_line, os.path.join(outdir, "iso_line.step"))
    # CIRCLE
    shape_circ = iso_step_from_circle(CircleSpec((0,0,0),(0,0,1),250), chord_tol_mm=5.0)
    export_step(shape_circ, os.path.join(outdir, "iso_circle.step"))
    # ARC
    shape_arc = iso_step_from_arc(ArcSpec((0,0,0),(0,0,1),250, 0, 90), chord_tol_mm=5.0)
    export_step(shape_arc, os.path.join(outdir, "iso_arc.step"))
    print("[OK] ISO STEP written to", outdir)


if __name__ == "__main__":
    # Default: run both
    run_ortho()
    run_iso()
    run_iso_step()