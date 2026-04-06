import FreeCAD as App
import FreeCADGui
import os
import importlib

class OPE_Iso_Gen_Cmd_Reload:
    def GetResources(self):
        return {
            'Pixmap': os.path.join(
            App.getResourceDir(), "Mod", "Part", "Resources", "icons", "PartWorkbench.svg"
        ) ,
            'MenuText': 'OPE Iso Gen Cmd Reload',
            'ToolTip': 'Does something useful'
        }

    def Activated(self):
        from importlib import reload
        import OPE_Iso_Gen.genBox
        reload(OPE_Iso_Gen.genBox)

    def IsActive(self):
        return True
