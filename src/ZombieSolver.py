"""
Solve Kangaroo2 goals using a custom iteration script ala
Zombie solver in K1. Open script to set solver variables.
    Inputs:
        GoalObjects: Kangaroo2 goals to solve {datatree,k2Goal}
    Outputs:
        GoalOutputs: GoalFunction Outputs {list,object}
    Remarks:
        Author: Anders Holden Deleuran (based on C# script by Daniel Piker)
        License: Apache License 2.0
        Version: 160402
"""

ghenv.Component.Name = "ZombieSolver"
ghenv.Component.NickName = "ZS"
ghenv.Component.Category = "CM_FAHS"
ghenv.Component.SubCategory = "3 Shaping"

import clr
clr.AddReferenceToFile("KangarooSolver.dll")
import KangarooSolver as ks
from System.Collections.Generic import List
import ahd

# Set global solve variables
threshold = 1e-13
maxIterations = 5000
tolerance = 0.0001
t = ahd.Timer()

if GoalObjects:
    
    # Make solver system and goals list
    ps = ks.PhysicalSystem()
    goals = List[ks.IGoal]()
    
    # Assign indexes to the particles in each Goal
    for g in GoalObjects:
        ps.AssignPIndex(g,tolerance) # points closer than second parameter will get combined into a single particle
        goals.Add(g)
        
    # Solve zombie style i.e. max N iterations, break when average movement drops below threshold
    i = 0
    t.start()
    while i < maxIterations:
        ps.Step(goals,False,1.0)
        i += 1
        if ps.GetvSum() < threshold:
            break
    solveTime = t.stop()
    
    # Output to GH
    GoalOutputs = ps.GetOutput(goals)
    Iterations = i
    SolveTime = solveTime
else:
    GoalOutputs = []