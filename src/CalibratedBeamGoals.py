"""
Make K2Engineering goals for defining a calibrated solid circular cross section beam.
    Inputs:
        Polylines: Polylines representing bending beam elements {list,polyline}
        YoungsModulus: The ratio of the stress (force per unit area) along an axis to the strain (N/mm2) {item,float}
        Density: The volumetric mass density (kg/m3) {item,float}
        Diameter: Diameter of cable in (mm) {item,float}
        BendAngleMin: The angle formed by two polyline edges must be larger/equal to this to be considered continuous {item,float}
    Outputs:
        G: Kangaroo2 goals representing behaviours {list,k2Goal}
    Remarks:
        Author: Anders Holden Deleuran
        License: Apache License 2.0
        Version: 201020
"""

ghenv.Component.Name = "CalibratedBeamGoals"
ghenv.Component.NickName = "CBG"
ghenv.Component.Category = "CM_FAHS"
ghenv.Component.SubCategory = "5 Structural"

import clr
import math
import Rhino as rc
import Grasshopper as gh
clr.AddReferenceToFileAndPath(gh.Folders.PluginFolder+"Components\KangarooSolver.dll")
clr.AddReferenceToFileAndPath(gh.Folders.DefaultAssemblyFolder+"K2Engineering.gha")
import KangarooSolver as ks
import K2Engineering as k2e
from collections import deque

def calcNodalSelfweight(bars,nodes,area,rho):
    
    # Initialise force array
    nodalForces = [rc.Geometry.Vector3d(0,0,0) for n in nodes]
    
    # force direction
    dir = rc.Geometry.Vector3d(0,0,-1)
    
    # Add forces resulting from each bar
    for l in bars:
        
        # Get index line start/end in nodes
        indexStart = nodes.IndexOf(nodes,l.From)
        indexEnd = nodes.IndexOf(nodes,l.To)
        
        edge = l.To - l.From
        length = edge.Length * 0.5
        
        force = dir * length * area * 1e-6 * rho * 9.82
        nodalForces[indexStart] += force
        nodalForces[indexEnd] += force
        
    return nodalForces

def calibratedBeamGoals(plc,youngsModulus,area,inertia,zDistance,rho,bendAngleMin,minSegLength):
    
    """ Make K2Structural goals for defining a bending beam element """
    
    # Return list
    goals = []
    
    # Convert to polyline and get segments and unique vertices
    if type(plc) is not rc.Geometry.Polyline:
        polyline = plc.TryGetPolyline()[1]
    vts = polyline.ToArray()
    uniqueVts = rc.Geometry.Point3d.CullDuplicates(vts,0.001)
    segs = deque(polyline.GetSegments())
    
    # Make bar goals (replacing K2 spring goal)
    for l in segs:
        if l.Length > minSegLength:
            g = k2e.Bar.BarGoal(l,youngsModulus*0.01,area)
            goals.append(g)
            
    # Make selfweight load goals
    loadVectors = calcNodalSelfweight(segs,uniqueVts,area,rho)
    for v,pt in zip(loadVectors,uniqueVts):
        g =  k2e.Load.LoadGoal(pt,v)
        goals.append(g)
        
    # Make rod goals (replacing K2 angle goal)
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
                    g = k2e.Rod.RodGoal(eA,eB,youngsModulus,inertia,zDistance,0)
                    goals.append(g) 
        segs.rotate(-1)
        
    # Make show/locator goal for outputting polyline from solver
    ghCrv = gh.Kernel.Types.GH_Curve(plc)
    gow = gh.Kernel.Types.GH_ObjectWrapper(ghCrv)
    gl = ks.Goals.Locator(gow)
    goals.append(gl)
    
    return goals


# Make output list and fill it with goals
if Polylines and Polylines[0]:
    
    # Calculate additional material properties
    area = math.pi * math.pow((Diameter/2),2)
    inertia = (math.pi * math.pow(Diameter,4))/64
    zDistance = Diameter/2
    
    # Make output list and populate with goals
    G = []
    for plc in Polylines:
        goals = calibratedBeamGoals(plc,YoungsModulus,area,inertia,zDistance,Density,BendAngleMin,0.00)
        G.extend(goals)
else:
    G = []