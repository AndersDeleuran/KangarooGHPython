"""
Solve Kangaroo2 goals using a custom iteration script.
Based on Daniel Pikers StepByStep.gh definition.
-
Author: Anders Holden Deleuran
Github: github.com/AndersDeleuran/KangarooGHPython
Updated: 150429
"""

import clr
clr.AddReferenceToFile("KangarooSolver.dll")
import KangarooSolver as ks
from System.Collections.Generic import List

# Reset state
if Reset or "counter" not in globals():
    
    # Make physical system and goals list (using .NET type list)
    ps = ks.PhysicalSystem()
    goalList = List[ks.IGoal]()
    
    # Add goals to system and goals list
    for g in Goals:
        ps.AssignPIndex(g,0.01)
        goalList.Add(g)
        
    # Make static counter variable
    counter = 0
        
# Run state
else:
    if Step:
        ps.Step(goalList,True, 1)
        counter += 1
        
# Output to GH
A = ps.GetOutput(goalList)
B = counter