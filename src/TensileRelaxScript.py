"""
Solve Kangaroo2 goals using a custom iteration script ala Zombie mode.
Based on Daniel Pikers TensileRelaxScript.gh definition.
-
This is quite a bit slower than the C# version, will have to profile deeper.
I suspect it might simply be the sum of all the KangarooSolver calls which 
become more apparent when solved zombie-style.
-
Author: Anders Holden Deleuran
Github: github.com/AndersDeleuran/KangarooGHPython
Updated: 150502
"""

import clr
clr.AddReferenceToFile("KangarooSolver.dll")
import KangarooSolver as ks
from System.Collections.Generic import List

# Make solver system and goals list
ps = ks.PhysicalSystem()
goals = List[ks.IGoal]()

# Get the mesh vertices and boundary status
pts = M.Vertices.ToPoint3dArray()
naked = M.GetNakedEdgePointStatus()

# Add vertices as particles and naked vertices as anchors
for i in range(M.Vertices.Count):
    ps.AddParticle(pts[i],1)
    if naked[i]:
        goals.Add(ks.Goals.Anchor(i,pts[i],10000))

# Add edges as springs
for i in range(M.TopologyEdges.Count):
    ends = M.TopologyEdges.GetTopologyVertices(i)
    start = M.TopologyVertices.MeshVertexIndices(ends.I)[0]
    end = M.TopologyVertices.MeshVertexIndices(ends.J)[0]
    goals.Add(ks.Goals.Spring(start,end,0,1))

# System state variables
counter = 0
threshold = 1e-6

# Solve zombie style i.e. max N iterations, break when system kinetic energy drops below threshold
while counter < 100:
    ps.Step(goals,True,threshold)
    counter += 1
    if ps.GetvSum() < threshold:
        break

# Replace the mesh vertices with the relaxed ones
M.Vertices.Clear()
M.Vertices.AddVertices(ps.GetPositions())

# Output the mesh, and how many iterations it took to converge
A = M
B = counter
