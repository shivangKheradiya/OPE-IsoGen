from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Optional

Pt3  = Tuple[float, float, float]
Vec3 = Tuple[float, float, float]


@dataclass(frozen=True)
class DimensionSpec:
    """
    DXF dimension contract (linear-aligned) with full configurability.

    P1, P2         → the extension points in 3D
    C              → dimension line anchor point in 3D (controls offset)
    n              → plane normal (defines the dimension plane)
    xdir           → baseline direction inside the plane

    text           → manual dimension text (if provided)
                     if None → auto compute |P2 - P1| (in mm)

    height_mm      → text height in mm
    layer          → DXF layer name

    arrow_style    → 'TICK' | 'OPEN' | 'CLOSED' | 'DOT' | 'NONE'

    text_position  → 'CENTER' | 'ABOVE' | 'INLINE'
                     CENTER → text centered on dimension line
                     ABOVE  → text offset above dim line ( +ydir )
                     INLINE → text sits on dimension line

    auto_text      → True = generate length automatically
                     False = use provided text exactly
    """

    P1: Pt3
    P2: Pt3
    C:  Pt3
    n: Vec3
    xdir: Vec3

    text: Optional[str] = None          # None → auto dim text
    height_mm: float = 4.0
    layer: str = "DIM"

    arrow_style: str = "TICK"           # default ISO tick marks
    text_position: str = "CENTER"       # CENTER | ABOVE | INLINE
    auto_text: bool = True              # auto compute if text is None