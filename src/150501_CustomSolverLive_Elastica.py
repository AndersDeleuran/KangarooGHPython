"""
Solve Kangaroo2 goals using a custom iteration script which runs "live".
Based on Daniel Pikers StepByStep.gh definition.
-
Author: Anders Holden Deleuran
Github: github.com/AndersDeleuran/KangarooGHPython
Updated: 150501
"""

import clr
clr.AddReferenceToFile("KangarooSolver.dll")
import KangarooSolver as ks
from System.Collections.Generic import List
import Grasshopper as gh

def ghComponentTimer(ghenv,pause,interval):
    
    """ Update the component at the interval like using a GH timer """
    
    # Ensure interval is larger than zero
    if interval <= 0:
        interval = 1
        
    # Get the Grasshopper document and component that owns this script
    ghComp = ghenv.Component
    ghDoc = ghComp.OnPingDocument()
    
    # Define the callback function
    def callBack(ghDoc):
        ghComp.ExpireSolution(False)
        
    # Update the solution
    if not pause:
        ghDoc.ScheduleSolution(interval,gh.Kernel.GH_Document.GH_ScheduleDelegate(callBack))


# Reset State
if Reset or "counter" not in globals():
    
    # Make physical system and goals list
    ps = ks.PhysicalSystem()
    goalList = List[ks.IGoal]()
    
    # Add goals to system and goals list
    for g in Goals:
        ps.AssignPIndex(g,0.01)
        goalList.Add(g)
        
    # Make static counter variable
    counter = 0
    
# Run State
else:
    
    # Solve n times at each GH iteration
    for i in range(Iterations):
        
        # Step the system
        ps.Step(goalList,True,1)
        
        # Get the velocity sum and increment the counter
        VSum = ps.GetvSum()
        counter += 1
        
        # Update the GH component
        ghComponentTimer(ghenv,Pause,5)
        
# Output the GH
GoalsOutput = ps.GetOutput(goalList)
Points = "foo"
Counter = counter