# src/OPE_IsoGen/Geometry/Primitives3D/dimension3d.py

from __future__ import annotations
import os
import ezdxf
import math
from typing import Tuple

from OCC.Core.gp import gp_Dir, gp_Pnt, gp_Ax3

from OPE_IsoGen.Geometry.Contracts.dimension_spec import DimensionSpec
from OPE_IsoGen.Geometry.Primitives3D.text3d import text3d_to_dxf
from OPE_IsoGen.Geometry.Contracts.text_spec import TextSpec

Vec3 = Tuple[float, float, float]
Pt3  = Tuple[float, float, float]


# --------------------------------------------------------------
# Small vector utils
# --------------------------------------------------------------
def _unit3(v: Vec3) -> Vec3:
    L = math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2]) or 1.0
    return (v[0]/L, v[1]/L, v[2]/L)

def _sub(a: Pt3, b: Pt3) -> Vec3:
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def _add(a: Pt3, b: Vec3) -> Pt3:
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def _cross(a: Vec3, b: Vec3) -> Vec3:
    return (
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0],
    )

def _dot(a: Vec3, b: Vec3) -> float:
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


# --------------------------------------------------------------
# Build OCCT Ax3 and extract basis U,V,N
# --------------------------------------------------------------
def _frame_from_n_xdir(n: Vec3, xdir: Vec3):
    """
    Build right-handed orthonormal frame (U,V,N)
    using OCCT gp_Ax3 for dimensional plane.
    """
    dn = gp_Dir(*n)
    dx = gp_Dir(*xdir)
    ax3 = gp_Ax3(gp_Pnt(0,0,0), dn, dx)

    ux = ax3.XDirection()
    uy = ax3.YDirection()
    uz = ax3.Direction()

    return (
        (ux.X(), ux.Y(), ux.Z()),
        (uy.X(), uy.Y(), uy.Z()),
        (uz.X(), uz.Y(), uz.Z()),
    )


# --------------------------------------------------------------
# Arrowhead drawing utilities (local 2D)
# --------------------------------------------------------------
def _arrow_tick(size: float):
    """
    Returns local 2D polyline for ISO tick: a simple slash "/"
    """
    # simple line from (-s/2, -s/2) to (s/2, s/2)
    s = size
    return [(-s*0.5, -s*0.5), (s*0.5, s*0.5)]

def _arrow_open(size: float):
    """
    Local 2D "open" arrow, V shape.
    """
    s = size
    return [(-s, -s*0.5), (0, 0), (-s, s*0.5)]

def _arrow_closed(size: float):
    """
    Local 2D filled triangle arrow.
    For DXF TEXT, we use outline only (no fill).
    """
    s = size
    return [(0,0), (-s, -s*0.5), (-s, +s*0.5), (0,0)]

def _arrow_dot(size: float):
    """
    Represent a dot as a small triangle approximation (DXF friendly).
    """
    s = size
    return [(0,0), (-s*0.3,-s*0.3), (-s*0.3,s*0.3), (0,0)]


# --------------------------------------------------------------
# Draw a local polyline transformed to 3D UCS
# --------------------------------------------------------------
def _draw_polyline_3d(msp, pts2d, C, U, V, layer):
    """
    pts2d: list of (x,y) in local dimension plane
    (C,U,V) define mapping to 3D:
       P3 = C + x*U + y*V
    """
    pl = []
    for (x,y) in pts2d:
        px = C[0] + x*U[0] + y*V[0]
        py = C[1] + x*U[1] + y*V[1]
        pz = C[2] + x*U[2] + y*V[2]
        pl.append((px,py,pz))
    msp.add_lwpolyline(pl, dxfattribs={"layer": layer})


# --------------------------------------------------------------
# The MAIN DXF dimension builder
# --------------------------------------------------------------
def dimension3d_to_dxf(spec: DimensionSpec, path: str):
    """
    Build a 3D linear aligned dimension.
    Fully DXF-based. No SVG/STEP.
    """

    # ----------------------------------------------------------
    # Prepare DXF
    # ----------------------------------------------------------
    doc = ezdxf.new(setup=True)
    msp = doc.modelspace()

    layer = spec.layer

    # ----------------------------------------------------------
    # Build local dimension plane basis U,V,N
    # ----------------------------------------------------------
    U, V, N = _frame_from_n_xdir(spec.n, spec.xdir)

    # ----------------------------------------------------------
    # Project P1, P2 into local dimension coordinates
    # ----------------------------------------------------------
    def proj(P: Pt3):
        dx = P[0] - spec.C[0]
        dy = P[1] - spec.C[1]
        dz = P[2] - spec.C[2]
        x2 = dx*U[0] + dy*U[1] + dz*U[2]
        y2 = dx*V[0] + dy*V[1] + dz*V[2]
        return (x2, y2)

    p1_2d = proj(spec.P1)
    p2_2d = proj(spec.P2)

    # dimension line is horizontal in local U-axis
    x1, y1 = p1_2d
    x2, y2 = p2_2d

    # y-values should ideally be same; use "spec.C" as reference
    # Dimension line offset is controlled by spec.C being offset
    # so we use a common y0 = y1==y2==dimline_y
    y0 = (y1 + y2) * 0.5

    # ----------------------------------------------------------
    # Arrowhead selection
    # ----------------------------------------------------------
    arrow_size = spec.height_mm * 0.8
    style = spec.arrow_style.upper()

    if style == "TICK":
        arrow_func = _arrow_tick
    elif style == "OPEN":
        arrow_func = _arrow_open
    elif style == "CLOSED":
        arrow_func = _arrow_closed
    elif style == "DOT":
        arrow_func = _arrow_dot
    else:
        arrow_func = lambda s: []   # NONE

    arrL = arrow_func(arrow_size)
    arrR = arrow_func(arrow_size)

    # ----------------------------------------------------------
    # Draw extension lines from P1, P2 up/down to dim line
    # ----------------------------------------------------------
    ext1 = [(x1, y1), (x1, y0)]
    ext2 = [(x2, y2), (x2, y0)]

    _draw_polyline_3d(msp, ext1, spec.C, U, V, layer)
    _draw_polyline_3d(msp, ext2, spec.C, U, V, layer)

    # ----------------------------------------------------------
    # Draw dimension line
    # ----------------------------------------------------------
    dimline = [(x1, y0), (x2, y0)]
    _draw_polyline_3d(msp, dimline, spec.C, U, V, layer)

    # ----------------------------------------------------------
    # Draw arrowheads
    # ----------------------------------------------------------
    # left arrow at (x1,y0)
    ptsL = [(px + x1, py + y0) for (px,py) in arrL]
    _draw_polyline_3d(msp, ptsL, spec.C, U, V, layer)

    # right arrow at (x2,y0)
    ptsR = [(px + x2, py + y0) for (px,py) in arrR]
    _draw_polyline_3d(msp, ptsR, spec.C, U, V, layer)

    # ----------------------------------------------------------
    # Prepare dimension text (auto or manual)
    # ----------------------------------------------------------
    if spec.auto_text:
        # length in mm (distance in 3D)
        dx = spec.P2[0] - spec.P1[0]
        dy = spec.P2[1] - spec.P1[1]
        dz = spec.P2[2] - spec.P1[2]
        L = math.sqrt(dx*dx + dy*dy + dz*dz)
        textval = f"{L:.2f}"
    else:
        textval = spec.text or ""

    # ----------------------------------------------------------
    # Determine text location
    # ----------------------------------------------------------
    midx = (x1 + x2) * 0.5

    if spec.text_position.upper() == "CENTER":
        text_pt_2d = (midx, y0)

    elif spec.text_position.upper() == "ABOVE":
        text_pt_2d = (midx, y0 + spec.height_mm * 1.2)

    else:  # INLINE
        text_pt_2d = (midx, y0)

    # Convert local 2D to full 3D anchor
    tx = spec.C[0] + text_pt_2d[0]*U[0] + text_pt_2d[1]*V[0]
    ty = spec.C[1] + text_pt_2d[0]*U[1] + text_pt_2d[1]*V[1]
    tz = spec.C[2] + text_pt_2d[0]*U[2] + text_pt_2d[1]*V[2]

    # ----------------------------------------------------------
    # Place text in 3D using your text3d builder
    # ----------------------------------------------------------
    text_spec = TextSpec(
        C=(tx, ty, tz),
        n=spec.n,
        xdir=spec.xdir,
        text=textval,
        height_mm=spec.height_mm,
        rot_deg=0.0,
        halign="CENTER",
        layer=spec.layer
    )

    # Use your text3d_to_dxf to add TEXT entity in correct 3D orientation.
    text3d_to_dxf(text_spec, path.replace(".dxf", "_text.dxf"))

    # ----------------------------------------------------------
    # Save main DXF file (dimension lines + arrows)
    # ----------------------------------------------------------
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    doc.saveas(path)
