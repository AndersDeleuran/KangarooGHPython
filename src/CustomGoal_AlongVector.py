"""
Custom Goal "Along Vector"
Based on Daniel Piker's CustomGoal_AlongVector.gh definition.
-
Author: Marcus Strube
Github: github.com/AndersDeleuran/KangarooGHPython
Updated: 160330
"""

import clr
from System import Array, Double

clr.AddReferenceToFile("KangarooSolver.dll")

import KangarooSolver as ks
import Rhino as rc

class CustomGoal(ks.GoalObject):
    def __init__(self, P0, P1, P2, T, k):
        self.PPos = Array[rc.Geometry.Point3d]([P0, P1, P2])
        self.Move = Array.CreateInstance(rc.Geometry.Vector3d, 3)
        self.Weighting = Array[Double]([k, k, k]) # ??
        self.t = T

    def Calculate(self, p):
        p0 = p[self.PIndex[0]].Position
        p1 = p[self.PIndex[1]].Position
        p2 = p[self.PIndex[2]].Position

        v0 = p2 - p0
        target = p0 + self.t*v0
        v1 = target - p1

        self.Move[1] = 0.5*v1
        self.Move[0] = -0.5*v1
        self.Move[2] = -0.5*v1

A = CustomGoal(P0, P1, P2, T, k)
