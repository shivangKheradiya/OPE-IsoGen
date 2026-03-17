from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple

Pt3 = Tuple[float, float, float]


@dataclass(frozen=True)
class TextSpec:
    """
    Universal text contract used by both ISO and ORTHO workflows.
    
    C         : anchor point in 3D model space (mm)
    n         : plane normal (used for ISO/ORTHO orientation)
    xdir      : in-plane direction that defines “text runs this way”
    text      : the actual text string (UTF-8)
    height_mm : text height in mm (DXF/SVG/font geometry)
    rot_deg   : additional rotation (in degrees) applied after projection
    halign    : horizontal alignment ('LEFT', 'CENTER', 'RIGHT')
    layer     : Layer in which text will be placed
    """

    C: Pt3
    n: Pt3
    xdir: Pt3
    text: str
    height_mm: float = 5.0
    rot_deg: float = 0.0
    halign: str = "LEFT"
    layer:str = "TEXT"