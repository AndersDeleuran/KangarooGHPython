"""
Solve Kangaroo2 goals using a custom iteration script ala Zombie mode.
Based on Daniel Pikers CustomIteration.gh definition.
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
tol = 0.0001 # Points closer than this will get combined into a single particle

# Assign indexes to the particles in each Goal
for g in x:
    ps.AssignPIndex(g,tol)
    goals.Add(g)

# System state variables
counter = 0
threshold = 1e-10

# Solve zombie style i.e. max N iterations, break when system kinetic energy drops below threshold
while counter < 100:
    ps.Step(goals,True,threshold)
    counter += 1
    if ps.GetvSum() < threshold:
        break

A = ps.GetOutput(goals)
B = counter
