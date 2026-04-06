import FreeCAD as App
import FreeCADGui
import os
import OPE_Iso_Gen.genBox

class OPE_Iso_Gen_Cmd:
    def GetResources(self):
        return {
            'Pixmap': os.path.join(
            App.getResourceDir(), "Mod", "Part", "Resources", "icons", "PartWorkbench.svg"
        ) ,
            'MenuText': 'OPE Iso Gen Cmd',
            'ToolTip': 'Does something useful'
        }

    def Activated(self):
        print("Hello from My Command!\n")
        print("Hi")
        OPE_Iso_Gen.genBox.genBox()


    def IsActive(self):
        return True
