import nhl # Import the Nitsche Hodge Laplace package
from ngsolve import *
from ngsolve.meshes import MakeStructured2DMesh
import pandas as pd

Cw = 12                                         # Set the Nitsche penalty parameter
orders = [1, 2, 3]                              # Set how many orders you wanna test
ns = [10, 15, 20, 25]                            # vertices per direction of geometry, translates to 1/n = h
g = CF((sin(x)*cos(1/4*y),                      # Set a manufactured solution
        -sin(3*y)*cos(3/2*x)))              
 

def createGeometry(n):
    structuredMeshUnitSquare = MakeStructured2DMesh(quads=False, nx=n, ny=n)
    return structuredMeshUnitSquare

results = []
for n in ns:
    mesh = createGeometry(n)
    for order in orders:
        u, p, ndofs, eX = nhl.hodgeLaplaceOneForms2D(mesh, g, order, Cw)
        results.append({'h': 1/n, 'ndofs':ndofs, 'order':order, 'eX':eX})

df_oneForms2D = pd.DataFrame(results)
df_oneForms2D.to_csv("data/oneForms2Ddata.csv", index=False)
