"""
Live Kangaroo2 solver implemented in IronPython.
    Inputs:
        Goals: List of K2 goals to solve {list,K2Goal/IronPythonList}
        SubSteps: How many times to call the solve step per Grasshopper iteration {item,int}
        Pause: Pause the solve loop {item,bool}
        Run: Switch the solver between run and reset state {item,bool}
    Outputs:
        SystemData: Data about the physical system (particle count, goal count, velocity sum, iterations) {list,object} 
        GoalsOutput: The output from the solved goals {list,object}
    Remarks:
        Authors: Anders Holden Deleuran
        License: Apache License 2.0
        Version: 201020
"""

ghenv.Component.Name = "Kangaroo2LiveSolver"
ghenv.Component.NickName ="K2LS"

import clr
import Grasshopper as gh
clr.AddReferenceToFileAndPath(gh.Folders.PluginFolder+"Components\KangarooSolver.dll")
import KangarooSolver as ks
from System.Collections.Generic import List

# Set global solver variables
tolerance = 0.001
threshold = 1e-13

def updateComponent():
    
    """ Updates this component, similar to using a grasshopper timer """
    
    # Define callback action
    def callBack(e):
        ghenv.Component.ExpireSolution(False)
        
    # Get grasshopper document
    ghDoc = ghenv.Component.OnPingDocument()
    
    # Schedule this component to expire
    ghDoc.ScheduleSolution(1,gh.Kernel.GH_Document.GH_ScheduleDelegate(callBack))

def flattenGoals(goals):
    
    """ Flatten the goals input from GH to unpack python "suitcases" """
    
    flatGoals = []
    for g in goals:
        if type(g) is list:
            flatGoals.extend(g)
        else:
            flatGoals.append(g)
            
    return flatGoals

def resetSystem(ps,goals,goalList,tolerance):
    
    """ Clear particles/goals of a K2 physical system and reassign goals """
    
    # Clear system particles and goals
    ps.ClearParticles()
    goalList.Clear()
    
    # Add goals to system and goals list
    for g in flattenGoals(goals):
        ps.AssignPIndex(g,tolerance)
        goalList.Add(g)

def solveSystem(ps,goals,goalList,tolerance,threshold,substeps):
    
    """ Solve the goals af a K2 physical system """
    
    # Read the goals again in case they have changed
    goalList.Clear()
    for g in flattenGoals(goals):
        if g.PIndex == None:
            ps.AssignPIndex(g,tolerance,False)
        goalList.Add(g)
        
    # Step the system N times each grasshopper iteration
    for i in range(substeps):
        ps.SimpleStep(goalList)
        
    # Get the velocity sum and set converged tag
    vSum = ps.GetvSum()
    if vSum <= threshold:
        converged = True
    else:
        converged = False
        
    return vSum,converged

# Make physical system and goals list (as persistent variables)
if "ps" not in globals():
    ps = ks.PhysicalSystem()
    goalList = List[ks.IGoal]()
    
# Reset state
if not Run:
    resetSystem(ps,Goals,goalList,tolerance)
    vSum = 0.0
    msg = None
    
# Run state
else:
    
    # Solve physical system
    vSum,converged = solveSystem(ps,Goals,goalList,tolerance,threshold,SubSteps)
    
    # Set component message
    msg = "Solver Running"
    if Pause:
        msg = "Solver Paused"
    if converged:
        msg = "System Converged"
        
    # Update component
    if not Pause:
        if not converged:
            updateComponent()
            
# Add component message
ghenv.Component.Message = msg

# Output to GH
GoalsOutput = ps.GetOutput(goalList)
SystemData = [ps.ParticleCount(),len(goalList),str(round(vSum,18)),ps.GetIterations()]