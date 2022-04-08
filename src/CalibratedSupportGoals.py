"""
Make Kangaroo2 goals for defining a support element.
    Inputs:
        Points: Polylines representing simple supports {list,point}
        X: Lock in X-axis {item,bool}
        Y: Lock in X-axis {item,bool}
        Z: Lock in X-axis{item,bool}
        Strength: Values representing the support strength {list,float}
    Outputs:
        G: Kangaroo2 goals representing behaviours {list,k2Goal}
    Remarks:
        Author: Anders Holden Deleuran
        License: Apache License 2.0
        Version: 201020
"""

ghenv.Component.Name = "CalibratedSupportGoals"
ghenv.Component.NickName = "CSG"
ghenv.Component.Category = "CM_FAHS"
ghenv.Component.SubCategory = "5 Structural"

import clr
import Grasshopper as gh
clr.AddReferenceToFileAndPath(gh.Folders.PluginFolder+"Components\KangarooSolver.dll")
clr.AddReferenceToFileAndPath(gh.Folders.DefaultAssemblyFolder+"K2Engineering.gha")
import KangarooSolver as ks
import K2Engineering as k2e

def makeSupportGoals(point,x,y,z,strength):
    
    """ Make K2Engineering goals for defining a support element """
    
    # Return list
    goals = []
    
    # Make anchor goal
    sg = k2e.Support.SupportGoal(point,x,y,z,float(strength))
    goals.append(sg)
    
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
        goals = makeSupportGoals(pt,X,Y,Z,Strength)
        G.extend(goals)
else:
    G = []