import clr
from System import Array, Double

clr.AddReferenceToFile("KangarooSolver.dll")

import KangarooSolver as ks
import Rhino as rc

class CustomGoal(ks.GoalObject):
    def __init__(self, line, Q, k):
        self.PPos = Array[rc.Geometry.Point3d]([line.From, line.To])
        self.Move = Array.CreateInstance(rc.Geometry.Vector3d, 2)
        self.Weighting = Array.CreateInstance(Double, 2)
        self.exponent = Q
        self.strength = k

    def Calculate(self, p):
        ptA = p[self.PIndex[0]].Position
        ptB = p[self.PIndex[1]].Position

        v = ptB - ptA
        d = v.Length
        v.Unitize()

        self.Move[0] = -v
        self.Move[1] = v

        self.Weighting[0] = self.Weighting[1] = d**self.exponent

GoalObject = [CustomGoal(line, Q, k) for line in L]
