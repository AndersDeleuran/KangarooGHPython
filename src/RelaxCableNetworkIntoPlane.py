"""
Relax a cable network into the XY plane using K2.
    Inputs:
        AssemblyGeo: The assembly geo to get the cable network from {datatree,object}
        MakePlanar: Forces the network fully planar {item,bool}
        Iterations: How many times to solve {item,int}
        SpringStrength: How much the cables should keep its original length {item,float}
        AngleStrength: How much to keep the cable network internal node angles at their ideal {item,float}
        PlaneStrength: How hard to oull the cable network nodes to the XY plane {item,float}
        OpenDegreeTwo: Rotates cables that touch degree two nodes by this amount {item,float}
        MakePlanar: Fully planarizes the network into the plane by zeroing the Z values {item,bool}
    Outputs:
        RelaxedNetwork: The flat cable network {list,line}
    Remarks:
        Author: Anders Holden Deleuran
        License: Apache License 2.0
        Version: 201104
"""

ghenv.Component.Name = "RelaxCableNetworkIntoPlane"
ghenv.Component.NickName ="RCNIP"
ghenv.Component.Category = "CM_FAHS"
ghenv.Component.SubCategory = "4 Topology"

import Rhino as rc
import Grasshopper as gh
import networkx as nx
import math
from collections import deque
from collections import Counter
import clr
clr.AddReferenceToFileAndPath(gh.Folders.PluginFolder+"Components\KangarooSolver.dll")
import KangarooSolver as ks
import Grasshopper.Kernel.Types as gkt
from System.Collections.Generic import List

def castEdges(edges):
    
    """ Cast edges to RhinoCommon line type """
    
    cEdges = []
    for e in edges:
        if type(e) is rc.Geometry.Line:
            cEdges.append(e)
        elif type(e) is rc.Geometry.LineCurve:
            cEdges.append(e.Line)
        elif type(e) is rc.Geometry.PolylineCurve or type(e) is rc.Geometry.NurbsCurve:
            l = rc.Geometry.Line(e.PointAtStart,e.PointAtEnd)
            cEdges.append(l)
    return cEdges

def openDegreeTwoNodes(cables,angle):
    
    """ Rotates cables that meet at a degree two nodes around their end point """
    
    # Get all vertices
    vts = []
    for l in cables:
        vts.append(l.From)
        vts.append(l.To)
        
    # Get valence two vertices
    valTwoVts = []
    for pt,n in Counter(vts).iteritems():
        if n == 2:
            valTwoVts.append(pt)
            
    # Adjust cables if start point in valence two nodes
    newCables = []
    rotAxis = rc.Geometry.Vector3d.ZAxis
    for l in cables:
        if l.From in valTwoVts:
            tr = rc.Geometry.Transform.Rotation(math.radians(angle),rotAxis,l.To)
            l.Transform(tr)
        newCables.append(l)
        
    return newCables

def rebuildLines(lines,roundDecimal):
    
    """ Rebuilds a list of lines to a tolerance decimal in place """
    
    for l in lines:
        l.FromX = round(l.FromX,roundDecimal)
        l.FromY = round(l.FromY,roundDecimal)
        l.FromZ = round(l.FromZ,roundDecimal)
        l.ToX = round(l.ToX,roundDecimal)
        l.ToY = round(l.ToY,roundDecimal)
        l.ToZ = round(l.ToZ ,roundDecimal)
        
        
def sortPointsAroundCenter(pts,center):
    
    """ Sort a list of points radially around a center """
    
    # Make plane through points and set its origin
    test,plane = rc.Geometry.Plane.FitPlaneToPoints(pts)
    plane.Origin = center
    
    # Calculate vectors from center to points
    vecs = [pt - center for pt in pts]
    
    # Calculate angles between vectors and plane X-axis
    angles = [rc.Geometry.Vector3d.VectorAngle(plane.XAxis,v,plane) for v in vecs]
    
    # Sort points by angles
    sortedBoth = sorted(zip(angles,pts))
    sortedPts = [l[1] for l in sortedBoth]
    
    return sortedPts,plane

def linesToGraph(lines,edgeMode):
    
    """ Creates a NetworkX graph from a list of lines """
    
    # Create graph
    graph = nx.Graph()
    
    # Get line endpoints
    endPts = []
    for l in lines:
        endPts.append(l.From)
        endPts.append(l.To)
        
    # Remove duplicate points and sort these
    uniquePts = list(set(endPts))
    uniquePts.sort()
    
    # Add nodes to graph
    for i,pt in enumerate(uniquePts):
        graph.add_node(i,point=pt)
        
    # Calculate the sum of all curve lengths
    sumCurveLengths = sum([l.Length for l in lines])
    avrCurveLengthPrc = (sumCurveLengths/len(lines))/sumCurveLengths
    
    # Add edges using edgeMode to determine the edge weight
    for l in lines:
        
        # Match the curve endpoints with the graph nodes
        startNode = uniquePts.index(l.From)
        endNode = uniquePts.index(l.To)
        
         # Calculate curve lenght percentage by all lines length
        lengthPrc = (l.Length/sumCurveLengths)
        
        # Add edge using metric distance i.e. curve length
        if edgeMode == "metric":            
            graph.add_edge(startNode,endNode,weight=lengthPrc,line=l) 
            
        # Or add edge using topological distance i.e. depth
        elif edgeMode == "average":            
            graph.add_edge(startNode,endNode,weight=avrCurveLengthPrc,line=l)
            
    return graph

def makeShowGoals(lines):
    
    """ Pass the cable lines through the solver """
    
    goals = []
    for l in lines:
        ghCrv = gkt.GH_Curve(l.ToNurbsCurve())
        gow = gkt.GH_ObjectWrapper(ghCrv)
        gl = ks.Goals.Locator(gow)
        goals.append(gl)
        
    return goals

def makeSpringGoals(lines,strength):
    
    """ Keep each cable its original length """
    
    goals = []
    for l in lines:
        g = ks.Goals.Spring(l.From,l.To,l.Length,strength)  
        goals.append(g)
    return goals

def makeOnPlaneGoals(graph,strength):
    
    """ Pull the cable network nodes to the XY plane """
    
    # Get node points
    nodePts = []
    for n in graph.nodes(data=True):
        nodePts.append(n[1]["point"])
        
    # Define plane
    plane = rc.Geometry.Plane.WorldXY
    
    # Make goals
    nodePts = List[rc.Geometry.Point3d](nodePts)
    goals = [ks.Goals.OnPlane(nodePts,plane,strength),]
    
    return goals

def makeAngleGoals(lineGraph,angleStrength):
    
    """ Keep the cable network internal node angles at their ideal """
    
    allAngleGoals = []
    for n in lineGraph.nodes():
        
        # Get node and neighbour points
        nodePt = lineGraph.node[n]["point"]
        neighbourPts = [lineGraph.node[n]["point"] for n in lineGraph.neighbors(n)]
        
        # Case B: Node has more than one neighbour
        if len(neighbourPts) > 1 :
            
            # Calculate ideal angle
            idealAngle = math.radians(360/len(neighbourPts))
            
            # Sort neighbours around around node
            neighbourPts,plane = sortPointsAroundCenter(neighbourPts,nodePt)
            
            # Make K2 angle goals to neighbours
            nLines = deque([rc.Geometry.Line(nPt,nodePt) for nPt in neighbourPts])
            nodeAngleGoals = []
            for i in range(len(nLines)):
                g = ks.Goals.Angle(nLines[0],nLines[1],idealAngle,angleStrength)
                nodeAngleGoals.append(g)
                nLines.rotate()
                
            # Add to output
            allAngleGoals.extend(nodeAngleGoals)
            
    return allAngleGoals

def solveGoals(goals,iterations,tol):
    
    """ Relax a line network using Kangaroo2 """
    
    if iterations == 0:
        return None
        
    else:
        
        # Make solver system and goals dotnet list
        ps = ks.PhysicalSystem()
        goalsList = List[ks.IGoal]()
        
        # Assign indexes to the particles in each Goal
        for g in goals:
            ps.AssignPIndex(g,tol)
            goalsList.Add(g)
            
        # Solve system
        for i in range(int(iterations)):
            ps.Step(goalsList,False,1000)
            
        # Get edges
        relaxedEdges = []
        for o in ps.GetOutput(goalsList):
            if type(o) is rc.Geometry.Line:
                relaxedEdges.append(o)
                
        return relaxedEdges

def makePlanar(lines):
    
    """ Forces the network fully planar """
    
    for l in lines:
        
        l.FromZ = 0
        l.ToZ = 0

if Toggle and AssemblyGeo.DataCount and AssemblyGeo.Branches[0]:
    
    # Unpack datatree and cast cables to lines
    cables,beams,anchors = [b for b in AssemblyGeo.Branches]
    cableLines = castEdges(cables)
    
    # Open degree/valence 2 nodes
    if OpenDegreeTwo:
        cableLines = openDegreeTwoNodes(cableLines,OpenDegreeTwo)
        
    # Rebuild to tolerance
    rebuildLines(cableLines,6)
    
    # Make graph representing cable network
    cnGraph = linesToGraph(cableLines,"metric")
    
    # Make K2 goals
    showGoals = makeShowGoals(cableLines)
    springGoals = makeSpringGoals(cableLines,SpringStrength)
    angleGoals = makeAngleGoals(cnGraph,AngleStrength)
    planeGoals = makeOnPlaneGoals(cnGraph,PlaneStrength)
    goals = showGoals + angleGoals + springGoals + planeGoals
    
    # Solve goals
    if Iterations:
        cableLines = solveGoals(goals,Iterations,0.0001)
        
    # Fully Planarize network
    if MakePlanar:
        makePlanar(cableLines)
        
    # Check the input/output edge lengths are okay
    checkLengths = []
    for crv,l in zip(cables,cableLines):
        checkLengths.append(abs(crv.GetLength() - l.Length) < 0.001)
    if False in checkLengths:
        RelaxedOkay = False
    else:
        RelaxedOkay = True
        
    # Output to GH
    RelaxedNetwork = cableLines
else:
    RelaxedNetwork = []
    RelaxedOkay = []