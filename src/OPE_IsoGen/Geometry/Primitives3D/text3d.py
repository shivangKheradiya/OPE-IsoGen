# src/OPE_IsoGen/Geometry/Primitives3D/text3d.py

from __future__ import annotations
import os
import ezdxf
from typing import Tuple
from OPE_IsoGen.Geometry.Contracts.text_spec import TextSpec
from OCC.Core.gp import gp_Vec, gp_Dir, gp_Ax3, gp_Pnt

Vec3 = Tuple[float, float, float]

def occt_basis_from_xdir_normal(xdir, normal):
    """
    xdir   = (x, y, z) baseline direction
    normal = (nx, ny, nz) plane normal
    Returns ux, uy, uz as Python tuples for ezdxf.
    """

    # Convert to OCCT directions
    dx = gp_Dir(*xdir)
    dn = gp_Dir(*normal)

    # Build coordinate system:
    # gp_Ax3(origin, normal, xdirection)
    ax3 = gp_Ax3(gp_Pnt(0, 0, 0), dn, dx)

    # Extract orthonormal basis
    ux = ax3.XDirection()
    uy = ax3.YDirection()
    uz = ax3.Direction()  # same as normal

    return (
        (ux.X(), ux.Y(), ux.Z()),
        (uy.X(), uy.Y(), uy.Z()),
        (uz.X(), uz.Y(), uz.Z()),
    )
def text3d_to_dxf(spec: TextSpec, path: str, layer: str = "TEXT"):
    doc = ezdxf.new(setup=True)
    msp = doc.modelspace()

    # Build orthonormal basis using OCCT
    ux, uy, uz = occt_basis_from_xdir_normal(spec.xdir, spec.n)

    # Create TEXT entity
    txt = msp.add_text(
        spec.text,
        dxfattribs={
            "height": spec.height_mm,
            "layer": layer,
            "rotation": float(spec.rot_deg),
        }
    )

    # Insert at origin in UCS
    txt.dxf.insert = (0, 0, 0)

    # Build UCS at world position
    Cx, Cy, Cz = spec.C
    ucs = ezdxf.math.UCS(origin=(Cx, Cy, Cz), ux=ux, uy=uy)

    # Transform text from UCS → WCS
    txt.transform(ucs.matrix)

    # Alignment
    try:
        txt.set_pos(txt.dxf.insert, align=spec.halign.upper())
    except Exception:
        pass

    # Save DXF
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    doc.saveas(path)