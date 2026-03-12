# Simple script to connect two symbols via the Python API (without CLI)
from OPE_IsoGen.symbols2d.pipe import StraightPipe2D, StraightPipe2DParams
from OPE_IsoGen.symbols2d.elbow90 import Elbow90_2D, Elbow90Params
from OPE_IsoGen.connect.engine import connect_parent_child
from OPE_IsoGen.exporters.svg2d import export_svg_2d

p = StraightPipe2D(StraightPipe2DParams(od_mm=100, length_mm=500))
e = Elbow90_2D(Elbow90Params(od_mm=100))

prims, markers = connect_parent_child(p, e, plane="XY", parent_angle=0.0, parent_at=(0,0))
export_svg_2d(prims, markers, "examples/connected.svg")
print("Wrote examples/connected.svg")
