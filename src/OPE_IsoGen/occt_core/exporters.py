# src/OPE_IsoGen/occt_core/exporters.py

import os
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve


def export_step(shape, path):
    wr = STEPControl_Writer()
    wr.Transfer(shape, STEPControl_AsIs)
    if wr.Write(path) == IFSelect_RetDone:
        print("[OK] STEP:", path)
    else:
        print("[ERR] STEP failed")


# simple 2D projection (top view)
def export_svg(shape, path):
    xs=[]; ys=[]; lines=[]

    exp = TopExp_Explorer(shape, TopAbs_EDGE)

    while exp.More():
        edge = exp.Current()
        crv = BRepAdaptor_Curve(edge)

        p1 = crv.Value(crv.FirstParameter())
        p2 = crv.Value(crv.LastParameter())

        x1, y1 = p1.X(), p1.Y()
        x2, y2 = p2.X(), p2.Y()

        xs += [x1,x2]
        ys += [y1,y2]

        lines.append(((x1,y1),(x2,y2)))
        exp.Next()

    if not xs:
        with open(path,"w") as f:
            f.write("<svg/>")
        return

    minx,maxx=min(xs),max(xs)
    miny,maxy=min(ys),max(ys)

    W=maxx-minx+40
    H=maxy-miny+40

    def tx(x): return x-minx+20
    def ty(y): return H-(y-miny+20)

    with open(path,"w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">')
        f.write('<g stroke="black" stroke-width="2" fill="none">')
        for (p1,p2) in lines:
            f.write(f'<line x1="{tx(p1[0]):.2f}" y1="{ty(p1[1]):.2f}" '
                    f'x2="{tx(p2[0]):.2f}" y2="{ty(p2[1]):.2f}"/>')
        f.write('</g></svg>')
    print("[OK] SVG:", path)