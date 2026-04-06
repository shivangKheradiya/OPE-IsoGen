import FreeCAD as App

def genBox():
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("OPE_Iso_Doc")

    box = doc.addObject("Part::Box", "IsoBox")
    box.Length = 100
    box.Width = 50
    box.Height = 30

    doc.recompute()