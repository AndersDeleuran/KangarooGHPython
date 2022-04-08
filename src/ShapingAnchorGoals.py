"""
Make Kangaroo2 goals for defining anchor point supports.
    Inputs:
        Points: Polylines representing simple supports {list,point}
        Strength: Values representing the support strength {list,float}
    Outputs:
        G: Kangaroo2 goals representing behaviours {list,k2Goal}
    Remarks:
        Author: Anders Holden Deleuran
        License: Apache License 2.0
        Version: 201020
"""

ghenv.Component.Name = "ShapingAnchorGoals"
ghenv.Component.NickName = "SAG"
ghenv.Component.Category = "CM_FAHS"
ghenv.Component.SubCategory = "3 Shaping"

import Grasshopper as gh
import clr
clr.AddReferenceToFileAndPath(gh.Folders.PluginFolder+"Components\KangarooSolver.dll")
import KangarooSolver as ks

def makeAnchorGoals(point,strength):
    
    """ Make Kangaroo2 goals for defining an anchor support element """
    
    # Return list
    goals = []
    
    # Make anchor goal
    ag = ks.Goals.Anchor(point,strength)
    goals.append(ag)
    
    # Make show/locator goal for outputting polyline from solver
    ghPt = gh.Kernel.Types.GH_Point(point)
    gow = gh.Kernel.Types.GH_ObjectWrapper(ghPt)
    gl = ks.Goals.Locator(gow)
    goals.append(gl)
    
    return goals

# Make output list and fill it with goals
if Points and Points[0]:
    G = []
    for i,pt in enumerate(Points):
        goals = makeAnchorGoals(pt,Strength)
        G.extend(goals)
else:
    G = []