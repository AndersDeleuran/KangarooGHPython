"""
Solve Kangaroo2 goals using a custom iteration script ala Zombie mode.
Based on Daniel Pikers CustomIteration.gh definition.
-
Author: Anders Holden Deleuran
Github: github.com/AndersDeleuran/KangarooGHPython
Updated: 160330
"""

import clr
from System.Collections.Generic import List

clr.AddReferenceToFile("KangarooSolver.dll")
import KangarooSolver as ks

TOLERANCE = 0.0001  # points closer than this get merged
MAX_ITER = 100  # simulation stops after max iterations

ps = ks.PhysicalSystem()
goals = List[ks.IGoal]()

for goal in GoalObjects:
    ps.AssignPIndex(goal, TOLERANCE)  # Assign indices to particles in each Goal
    goals.Add(goal)

counter = 0
while counter < MAX_ITER:
    counter += 1

    ps.Step(goals, parallel=False, ke=Threshold)  # parallel is slower here. 
    if ps.GetvSum() < Threshold:
        break  # simulation stops when kinetic energy drops below threshold

O = ps.GetOutput(goals)
