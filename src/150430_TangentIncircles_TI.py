"""
How to make and output Kangaroo2 goals.
-
Author: Anders Holden Deleuran
Github: github.com/AndersDeleuran/KangarooGHPython
Updated: 150429
"""

# Add reference to the Kangaroo dll
import clr
clr.AddReferenceToFile("KangarooSolver.dll")

# Import the Kangaroo namespace using an alias
import KangarooSolver as ks

# Make empty output list
TI = []

# Iterate inputs and make goals
for i in range(len(A)):
    g = ks.Goals.TangentIncircles(A[i],C[i],B[i],D[i],10.0)
    
    # Add to output list
    TI.append(g)