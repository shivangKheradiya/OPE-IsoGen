from dataclasses import dataclass
from OCC.Core.gp import gp_Ax2, gp_Pnt, gp_Dir
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder

@dataclass
class StraightPipeParams:
    od_mm: float = 100.0   # outer diameter (mm)
    length_mm: float = 500.0

class StraightPipeSymbol:
    """
    Minimal straight pipe represented as a solid cylinder (OD only for now).
    Later we'll add thickness (ID), material, spec, etc.
    """

    def __init__(self, params: StraightPipeParams | None = None):
        self.params = params or StraightPipeParams()

    def build_shape_3d(self):
        """Return a TopoDS_Shape (solid cylinder)."""
        r = self.params.od_mm / 2.0
        L = self.params.length_mm

        # Cylindrical axis along +Z, origin at (0,0,0)
        ax2 = gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))
        mk_cyl = BRepPrimAPI_MakeCylinder(ax2, r, L)
        shape = mk_cyl.Shape()
        return shape

    def render_svg_preview(self):
        """
        TEMPORARY: super-simple SVG preview (a rectangle) to prove the pipeline works.
        This is NOT the true isometric projection yet.
        """
        w = int(self.params.length_mm)
        h = int(self.params.od_mm)
        w = max(50, min(w, 800))  # clamp so it stays visible
        h = max(10, min(h, 200))
        return f'''
<svg width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">
  <rect x="1" y="1" width="{w-2}" height="{h-2}"
        fill="none" stroke="blue" stroke-width="2"/>
  <text x="6" y="{min(h-6, 18)}" font-size="12"
        font-family="Arial" fill="blue">
    StraightPipe (OD={self.params.od_mm}mm, L={self.params.length_mm}mm)
  </text>
</svg>
'''.strip()