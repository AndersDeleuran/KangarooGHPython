"""
How to make and output Kangaroo2 goals.
-
Author: Anders Holden Deleuran
Github: github.com/AndersDeleuran/KangarooGHPython
Updated: 150429
"""

import clr
clr.AddReferenceToFile("KangarooSolver.dll")
import KangarooSolver as ks
import Rhino as rc
from System.Collections.Generic import List

# Convert Python points list to .NET type list
ptsList = List[rc.Geometry.Point3d](Pts)

# Make the OnPlane goal and output to GH
P = ks.Goals.OnPlane(ptsList,rc.Geometry.Plane.WorldXY,1.0)