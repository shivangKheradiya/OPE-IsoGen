# src/OPE_IsoGen/occt_core/builder.py

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeWire
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopoDS import TopoDS_Compound

from ..pipeline.attribute_codes import TYPE, PIPE, START_X,START_Y,START_Z,END_X,END_Y,END_Z
from .pipe import build_pipe_edge


def build_pipeline_shape(items):
    edges = []

    for it in items:
        comp = int(it[TYPE])

        if comp == PIPE:
            S = (it[START_X], it[START_Y], it[START_Z])
            E = (it[END_X],   it[END_Y],   it[END_Z])
            edges.append(build_pipe_edge(S,E))

        else:
            print("[INFO] Component not supported yet:", comp)

    # Try assembling into a wire
    wire_mk = BRepBuilderAPI_MakeWire()
    for e in edges:
        wire_mk.Add(e)

    if wire_mk.IsDone():
        return wire_mk.Wire()

    # Fallback: compound
    comp_shape = TopoDS_Compound()
    b = BRep_Builder()
    b.MakeCompound(comp_shape)
    for e in edges:
        b.Add(comp_shape, e)

    return comp_shape