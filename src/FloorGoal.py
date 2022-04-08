"""
Make Kangaroo2 goal for defining a floor which will work with the Zombie solver.
    Inputs:
        Toggle: Enables the component {item,bool}
        Strength: The goal strength {list,float}
    Outputs:
        G: Kangaroo2 goals representing behaviours {list,k2Goal}
    Remarks:
        Author: Anders Holden Deleuran
        License: Apache License 2.0
        Version: 201020
"""

ghenv.Component.Name = "FloorGoal"
ghenv.Component.NickName = "FG"
ghenv.Component.Category = "CM_FAHS"
ghenv.Component.SubCategory = "5 Structural"

import clr
import Rhino as rc
import Grasshopper as gh
clr.AddReferenceToFileAndPath(gh.Folders.PluginFolder+"Components\KangarooSolver.dll")
import KangarooSolver as ks
from System import Array

if Toggle and Strength:
    G = ks.Goals.FloorPlane(Strength)
    G.PPos = Array[rc.Geometry.Point3d]((rc.Geometry.Point3d(0,0,0),))
else: G = []