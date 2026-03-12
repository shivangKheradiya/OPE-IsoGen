from __future__ import annotations
from typing import List
from ..geometry2d.primitives import Line2D, Polyline2D, Marker2D

def export_svg_2d(prims: List, markers: List[Marker2D], path: str, padding: float = 24.0):
    # Compute bounds
    xs, ys = [], []
    for p in prims:
        if isinstance(p, Line2D):
            xs += [p.x1, p.x2]; ys += [p.y1, p.y2]
        elif isinstance(p, Polyline2D):
            for (x,y) in p.points:
                xs.append(x); ys.append(y)
    for m in markers or []:
        xs.append(m.x); ys.append(m.y)
    if not xs: xs=[0.0]; 
    if not ys: ys=[0.0]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    width  = (maxx - minx) + 2*padding
    height = (maxy - miny) + 2*padding

    def tx(x): return (x - minx) + padding
    def ty(y): return height - ((y - miny) + padding)  # flip Y for SVG

    out = []
    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{max(1,int(width))}" height="{max(1,int(height))}">')
    out.append('<g stroke="black" stroke-width="2" fill="none">')

    for p in prims:
        if isinstance(p, Line2D):
            out.append(f'<line x1="{tx(p.x1):.2f}" y1="{ty(p.y1):.2f}" x2="{tx(p.x2):.2f}" y2="{ty(p.y2):.2f}"/>')
        elif isinstance(p, Polyline2D):
            if len(p.points) >= 2:
                d = " ".join(f"{tx(x):.2f},{ty(y):.2f}" for (x,y) in p.points)
                out.append(f'<polyline points="{d}" fill="none" stroke="black" stroke-width="2"/>')

    out.append('</g>')

    # Markers
    out.append('<g fill="red" stroke="none">')
    for m in markers or []:
        out.append(f'<circle cx="{tx(m.x):.2f}" cy="{ty(m.y):.2f}" r="3"/>')
        if m.label:
            out.append(f'<text x="{tx(m.x)+6:.2f}" y="{ty(m.y)-6:.2f}" font-size="12" fill="red">{m.label}</text>')
    out.append('</g>')

    out.append('</svg>')

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))