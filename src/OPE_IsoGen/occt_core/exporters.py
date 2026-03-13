# src/OPE_IsoGen/occt_core/exporters.py

import os
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from .projector import iso_project_point

ISO = True

def export_step(shape, path):
    wr = STEPControl_Writer()
    wr.Transfer(shape, STEPControl_AsIs)
    if wr.Write(path) == IFSelect_RetDone:
        print("[OK] STEP:", path)
    else:
        print("[ERR] STEP failed")