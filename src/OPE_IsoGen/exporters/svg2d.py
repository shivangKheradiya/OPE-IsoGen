from __future__ import annotations
from typing import List
import math
from OPE_IsoGen.geometry2d.primitives import Line2D, Arc2D, Marker2D

def export_svg_2d(prims: List, markers: List[Marker2D], path: str, padding: float = 20.0):
    # Compute bounds
    xs, ys = [], []
    for p in prims + markers:
        if isinstance(p, Line2D):
            xs += [p.x1, p.x2]; ys += [p.y1, p.y2]
        elif isinstance(p, Arc2D):
            # Sample arc ends & middle for a simple bbox
            a1, a2 = math.radians(p.start_deg), math.radians(p.end_deg)
            xm = p.cx + p.r * math.cos((a1 + a2) / 2.0)
            ym = p.cy + p.r * math.sin((a1 + a2) / 2.0)
            xs += [p.cx + p.r * math.cos(a1), p.cx + p.r * math.cos(a2), xm]
            ys += [p.cy + p.r * math.sin(a1), p.cy + p.r * math.sin(a2), ym]
        elif isinstance(p, Marker2D):
            xs.append(p.x); ys.append(p.y)
    if not xs: xs = [0]; 
    if not ys: ys = [0]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    width  = (maxx - minx) + 2 * padding
    height = (maxy - miny) + 2 * padding

    def tx(x): return (x - minx) + padding
    def ty(y): return height - ((y - miny) + padding)  # flip Y for SVG

    # Build SVG
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{max(1,int(width))}" height="{max(1,int(height))}">']
    parts.append('<g stroke="black" stroke-width="2" fill="none">')
    for p in prims:
        if isinstance(p, Line2D):
            parts.append(f'<line x1="{tx(p.x1):.2f}" y1="{ty(p.y1):.2f}" x2="{tx(p.x2):.2f}" y2="{ty(p.y2):.2f}"/>')
        elif isinstance(p, Arc2D):
            # SVG arc path: we’ll create a path using absolute arc command
            a1 = math.radians(p.start_deg)
            a2 = math.radians(p.end_deg)
            x1, y1 = p.cx + p.r*math.cos(a1), p.cy + p.r*math.sin(a1)
            x2, y2 = p.cx + p.r*math.cos(a2), p.cy + p.r*math.sin(a2)
            large_arc = 1 if (abs(p.end_deg - p.start_deg) % 360) > 180 else 0
            sweep = 1 if p.end_deg >= p.start_deg else 0
            parts.append(
                f'<path d="M {tx(x1):.2f} {ty(y1):.2f} A {p.r:.2f} {p.r:.2f} 0 {large_arc} {sweep} {tx(x2):.2f} {ty(y2):.2f}"/>'
            )
    parts.append('</g>')
    # Markers (connection points)
    parts.append('<g fill="red" stroke="none">')
    for m in markers:
        parts.append(f'<circle cx="{tx(m.x):.2f}" cy="{ty(m.y):.2f}" r="3"/>')
        if m.label:
            parts.append(f'<text x="{tx(m.x)+6:.2f}" y="{ty(m.y)-6:.2f}" font-size="12" fill="red">{m.label}</text>')
    parts.append('</g>')
    parts.append('</svg>')

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))