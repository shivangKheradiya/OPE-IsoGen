"""Initialization of the OPE_Iso_Gen Workbench graphical interface."""

import FreeCAD as App
import FreeCADGui as Gui
import os

class OPE_Iso_GenWorkbench(Gui.Workbench):
    """OPE_Iso_Gen workbench object."""

    def __init__(self):
        self.__class__.Icon = os.path.join(
            App.getResourceDir(), "Mod", "Part", "Resources", "icons", "PartWorkbench.svg"
        ) 
        # "OPE_Iso_GenWorkbench.svg"
        self.__class__.MenuText = "OPE_Iso_Gen"
        self.__class__.ToolTip = "OPE_Iso_Gen workbench"


    def Initialize(self):
        # load the module
        from Commands.OPE_Iso_Gen_Cmd import OPE_Iso_Gen_Cmd
        from Commands.OPE_Iso_Gen_Cmd_Reload import OPE_Iso_Gen_Cmd_Reload
        Gui.addCommand('OPE_Iso_Gen_Cmd', OPE_Iso_Gen_Cmd())
        Gui.addCommand('OPE_Iso_Gen_Cmd_Reload', OPE_Iso_Gen_Cmd_Reload())
        print("OPE_Iso_Gen Workbench initialized.\n")

    def GetClassName(self):
        App.Console.PrintMessage("OPE_Iso_Gen Get ClassName Called")
        return "Gui::PythonWorkbench"

Gui.addWorkbench(OPE_Iso_GenWorkbench())