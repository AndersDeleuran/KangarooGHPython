"""
Make Kangaroo2 goals for shaping a beam element.
    Inputs:
        Polylines: Polylines representing bending beam elements {list,polylinecurve}
        TargetLengths: Values representing the target length of each polyline {list,float, optional}
        SpringStrength: Spring strength i.e. spring/length goal for each edge {item,float}
        BendStrength: Bending strength i.e. angle goal for consecutive edges {item,float}
        BendAngleMin: The angle formed by two polyline edges must be larger/equal to this to be considered continuous {item,float}
        MinSegLength: The shortest a polyline segment can be in order for it to be part of a goal [item,float}
    Outputs:
        G: Kangaroo2 goals representing behaviours {list,k2Goal}
    Remarks:
        Author: Anders Holden Deleuran
        License: Apache License 2.0
        Version: 201020
"""

ghenv.Component.Name = "ShapingBeamGoals"
ghenv.Component.NickName = "SBG"
ghenv.Component.Category = "CM_FAHS"
ghenv.Component.SubCategory = "3 Shaping"

import Rhino as rc
import Grasshopper as gh
import clr
clr.AddReferenceToFileAndPath(gh.Folders.PluginFolder+"Components\KangarooSolver.dll")
import KangarooSolver as ks
from collections import deque
import math

def shapingBeamGoals(curve,totalLength,springStrength,bendStrength,bendAngleMin,minSegLength):
    
    """ Make Kangaroo2 spring/angle/show goals for defining a bending element """
    
    # Return list
    goals = []
    
    # Convert to polyline and get segments
    if type(curve) is not rc.Geometry.Polyline:
        polyline = curve.TryGetPolyline()[1]
    segs = deque(polyline.GetSegments())
    
    # Calculate springs rest lengths
    if totalLength:
        lf = totalLength/polyline.Length
        restLengths = [l.Length*lf for l in segs]
    else:
        restLengths = [l.Length for l in segs]
        
    # Calculate springs strength
    ss = springStrength*len(segs)
    
    # Make spring goals
    for l,rl in zip(segs,restLengths):
        if l.Length > minSegLength:
            goals.append(ks.Goals.Spring(l.From,l.To,rl,ss))
        
    # Make angle goals
    for i in range(len(segs)):
        
        # Get segments and segment vectors 
        eA = segs[0]
        eB = segs[1]
        vA = eA.To-eA.From
        vB = eB.From-eB.To
        
        # Check edge length
        if eA.Length > minSegLength and eB.Length > minSegLength:
            
            # Check that edges connect and their angle is larger than min bend angle
            if eA.To == eB.From:
                if math.degrees(rc.Geometry.Vector3d.VectorAngle(vA,vB)) > bendAngleMin + 1:
                    #goals.append(ks.Goals.Angle(eA,eB,0.00,bendStrength)) 
                    goals.append(ks.Goals.Angle2(eA,eB,0.00,bendStrength))
                
        segs.rotate(-1)
        
    # Make show/locator goal for outputting polyline from solver
    ghCrv = gh.Kernel.Types.GH_Curve(curve)
    gow = gh.Kernel.Types.GH_ObjectWrapper(ghCrv)
    gl = ks.Goals.Locator(gow)
    goals.append(gl)
    
    return goals


# Make output list and fill it with goals
if Polylines and Polylines[0]:
    G = []
    for i,plc in enumerate(Polylines):
        if len(Polylines) == len(TargetLengths):
            goals = shapingBeamGoals(plc,TargetLengths[i],SpringStrength,BendStrength,BendAngleMin,0.00)
        else:
            goals = shapingBeamGoals(plc,None,SpringStrength,BendStrength,BendAngleMin,0.00)
        G.extend(goals)
else:
    G = []