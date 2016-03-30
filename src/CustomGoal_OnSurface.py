import clr
from System import Array, Double

clr.AddReferenceToFile("KangarooSolver.dll")

import KangarooSolver as ks
import Rhino as rc

class CustomGoal(ks.GoalObject):
    def __init__(self, P, S, k):
        self.PPos = Array[rc.Geometry.Point3d]([P])
        self.Move = Array.CreateInstance(rc.Geometry.Vector3d, 1)
        self.Weighting = Array[Double]([k])
        self.brep = S

    def Calculate(self, p):
        pt = p[self.PIndex[0]].Position
        self.Move[0] = self.brep.ClosestPoint(pt) - pt

GoalObject = CustomGoal(P, S, k)
