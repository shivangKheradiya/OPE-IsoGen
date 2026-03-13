# src/OPE_IsoGen/occt_core/pipe.py

from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge

def build_pipe_edge(S, E):
    return BRepBuilderAPI_MakeEdge(
        gp_Pnt(*S),
        gp_Pnt(*E)
    ).Edge()