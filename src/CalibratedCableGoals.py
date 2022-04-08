"""
Make K2Engineering goals for defining a calibrated cable element.
    Inputs:
        Polylines: Polylines representing cable elements {list,polyline}
        YoungsModulus: The ratio of the stress (force per unit area) along an axis to the strain (N/mm2) {item,float}
        Density: The volumetric mass density (kg/m3) {item,float}
        Diameter: Diameter of cable in (mm) {item,float}
        Prestress: Pre-tension the cable (kN) {item,float}
    Outputs:
        G: Kangaroo2 goals representing behaviours {list,k2Goal}
    Remarks:
        Author: Anders Holden Deleuran
        License: Apache License 2.0
        Version: 201020
"""

ghenv.Component.Name = "CalibratedCableGoals"
ghenv.Component.NickName = "CCG"
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

def calibratedCableGoals(plc,youngsModulus,area,prestress,rho):
    
    """ Make K2Structural goals for defining a cable element """
    
    # Return list
    goals = []
    
    # Convert to polyline and get segments
    if type(plc) is not rc.Geometry.Polyline:
        polyline = plc.TryGetPolyline()[1]
    vts = polyline.ToArray()
    uniqueVts = rc.Geometry.Point3d.CullDuplicates(vts,0.001)
    segs = polyline.GetSegments()
    
    # Make cable goals (replacing springs)
    for l in segs:
        
        # Make the cable
        g = k2e.Cable.CableGoal(l,youngsModulus*0.01,area,prestress)
        goals.append(g)
        
    # Make selfweight load goals
    loadVectors = calcNodalSelfweight(segs,uniqueVts,area,rho)
    for v,pt in zip(loadVectors,uniqueVts):
        g =  k2e.Load.LoadGoal(pt,v)
        goals.append(g)
    
    # Make show/locator goal for outputting polyline from solver
    ghCrv = gh.Kernel.Types.GH_Curve(plc)
    gow = gh.Kernel.Types.GH_ObjectWrapper(ghCrv)
    gl = ks.Goals.Locator(gow)
    goals.append(gl)
    
    return goals

# Check inputs from GH
if Polylines and not None in Polylines:
    
    # Calculate additional material properties
    area = math.pi * math.pow((Diameter/2),2)
    prestressKN = Prestress/1000 # Not sure this is correct, have to check K2Engineering Git
    
    # Make output list and fill it with K2 structural goals
    G = []
    for plc in Polylines:
        goals = calibratedCableGoals(plc,YoungsModulus,area,prestressKN,Density)
        G.extend(goals)
else:
    G = []