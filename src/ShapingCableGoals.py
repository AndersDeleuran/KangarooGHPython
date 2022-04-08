"""
Make Kangaroo2 goals for shaping a cable element.
    Inputs:
        Polylines: Polylines representing bending beam elements {list,polylinecurve}
        TargetLengths: Values representing the target length of each polyline {list,float,optional}
        SpringStrength: Spring strength i.e. spring/length goal for each edge {item,float}
    Outputs:
        G: Kangaroo2 goals representing behaviours {list,k2Goal}
    Remarks:
        Author: Anders Holden Deleuran
        License: Apache License 2.0
        Version: 201020
"""

ghenv.Component.Name = "ShapingCableGoals"
ghenv.Component.NickName = "SCG"
ghenv.Component.Category = "CM_FAHS"
ghenv.Component.SubCategory = "3 Shaping"

import Rhino as rc
import Grasshopper as gh
import clr
clr.AddReferenceToFileAndPath(gh.Folders.PluginFolder+"Components\KangarooSolver.dll")
import KangarooSolver as ks

def makeCableElementGoals(curve,totalLength,strength):
    
    """ Make Kangaroo2 spring/show goals for defining a cable element """
    
    # Return list
    goals = []
    
    # Convert to polyline and get segments
    if type(curve) is not rc.Geometry.Polyline:
        polyline = curve.TryGetPolyline()[1]
    segs = polyline.GetSegments()
    
    # Calculate springs rest lengths
    if totalLength is not None:
        segL = totalLength / len(segs)
        restLengths = [segL for l in segs]
    else:
        restLengths = [l.Length for l in segs]
        
    # Calculate springs strength
    s = strength*len(segs)
    
    # Make spring goals
    for l,rl in zip(segs,restLengths):
        g = ks.Goals.Spring(l.From,l.To,rl,s)
        #g.Name = "cableSpring"
        goals.append(g)
        
    # Make show/locator goal for outputting polyline from solver
    ghCrv = gh.Kernel.Types.GH_Curve(curve)
    gow = gh.Kernel.Types.GH_ObjectWrapper(ghCrv)
    gl = ks.Goals.Locator(gow)
    gl.Name = "cablePolyline"
    goals.append(gl)
    
    return goals


# Make output list and fill it with goals
if Polylines and Polylines[0]:
    G = []
    for i,plc in enumerate(Polylines):
        if len(Polylines) == len(TargetLengths):
            goals = makeCableElementGoals(plc,TargetLengths[i],SpringStrength)
        else:
            goals = makeCableElementGoals(plc,None,SpringStrength)
        G.extend(goals)
else:
    G = []