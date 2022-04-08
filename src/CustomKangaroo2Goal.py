"""
Working prototype for writing custom Kangaroo2 goals in IronPython. Note
that this solves substantially slower than C# goals (about three times on my
system), which may be an implementation detail (e.g. with the .NET Array and
Double types) or simply the cost of dynamic modelling with dynamic languages!
    Inputs:
        Lines: Lines to make springs from {list,line}
        Length: Rest length of springs {item,float}
    Outputs:
        G: K2 goals {list,goal}
    Remarks:
        Authors: Anders Holden Deleuran, Will Pearson
        License: Apache License 2.0
        Version: 220106
"""

ghenv.Component.Name = "CustomKangaroo2Goal"
ghenv.Component.NickName ="CK2G"

import clr
import Rhino as rc
import Grasshopper as gh
clr.AddReferenceToFileAndPath(gh.Folders.PluginFolder+"Components\KangarooSolver.dll")
import KangarooSolver as ks
from System import Array,Double

class Spring(ks.GoalObject):
    
    """ Class that replicates the standard K2 spring/length goal """
    
    def __init__(self,line,restLength,stiffness):
        
        self.PPos = Array[rc.Geometry.Point3d]((line.From,line.To))
        self.Move = Array.CreateInstance(rc.Geometry.Vector3d,2)
        self.Weighting = Array.CreateInstance(Double,2)
        self.RestLength = restLength
        self.Stiffness = stiffness
        
    def Calculate(self,p):
        current = p[self.PIndex.GetValue(1)].Position - p[self.PIndex.GetValue(0)].Position
        stretchfactor = 1.0 - self.RestLength / current.Length
        springMove = 0.5 * current * stretchfactor
        self.Move.SetValue(springMove,0)
        self.Move.SetValue(-springMove,1)
        self.Weighting.SetValue(2*self.Stiffness,0)
        self.Weighting.SetValue(2*self.Stiffness,1)
        
    def Output(self,p):
        l = rc.Geometry.Line(p[self.PIndex.GetValue(0)].Position,p[self.PIndex.GetValue(1)].Position)
        return l

G = [Spring(l,Length,1000.0) for l in Lines]