"""
How to make and output Kangaroo2 goals.
-
Author: Anders Holden Deleuran
Github: github.com/AndersDeleuran/KangarooGHPython
Updated: 150429
"""

import Grasshopper as gh
import clr
clr.AddReferenceToFile("KangarooSolver.dll")
import KangarooSolver as ks

# Make empty output list
GL = []

# Iterate inputs and make goals
for geo in G:
    gow = gh.Kernel.Types.GH_ObjectWrapper(gh.Kernel.Types.GH_Mesh(geo)) # Must be a more general way of doing this
    gl = ks.Goals.Locator(gow)
    GL.append(gl)