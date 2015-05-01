"""
How to make and output Kangaroo2 goals.
-
Author: Anders Holden Deleuran
Github: github.com/AndersDeleuran/KangarooGHPython
Updated: 150501
"""

import Rhino as rc
import clr
clr.AddReferenceToFile("KangarooSolver.dll")
import KangarooSolver as ks
import Grasshopper.Kernel.Types as gkt

# Make empty output list
GL = []

# Iterate inputs and make locator goals
for geo in G:
    
    if isinstance(geo,rc.Geometry.Mesh):
        gGh = gkt.GH_Mesh(geo)
        
    elif isinstance(geo,rc.Geometry.Point3d):
        gGh = gkt.GH_Point(geo)
        
    gow = gkt.GH_ObjectWrapper(gGh)
    gl = ks.Goals.Locator(gow) # Does this need to know about Grasshopper types?
    GL.append(gl)