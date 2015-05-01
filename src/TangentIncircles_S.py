"""
How to make and output Kangaroo2 goals.
-
Author: Anders Holden Deleuran
Github: github.com/AndersDeleuran/KangarooGHPython
Updated: 150501
"""

import Rhino as rc
import Grasshopper as gh
import clr
clr.AddReferenceToFile("KangarooSolver.dll")
import KangarooSolver as ks

# Make empty output list
GL = []

# Iterate inputs and make goals
for g in G:
    
    if isinstance(g,rc.Geometry.Mesh):
        gGh = gh.Kernel.Types.GH_Mesh(g)
        
    elif isinstance(g,rc.Geometry.Point3d):
        gGh = gh.Kernel.Types.GH_Point(g)
        
    gow = gh.Kernel.Types.GH_ObjectWrapper(gGh) # Must already be a more general way of doing this
    gl = ks.Goals.Locator(gow)
    GL.append(gl)
