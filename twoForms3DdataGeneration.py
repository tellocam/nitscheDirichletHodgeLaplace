import nhl # Import the Nitsche Hodge Laplace package
from ngsolve import *
from ngsolve.meshes import MakeStructured3DMesh
import pandas as pd

Cw = 12                                         # Set the Nitsche penalty parameter
orders = [1, 2]                                 # Set how many orders you wanna test
ns = [2, 3, 4, 6]                               # vertices per direction of geometry, translates to 1/n = h
g = CF((7*sin(x)*cos(y)*sin(2*z),               # Set a manufactured solution
        -cos(x)*sin(1/3*y)*cos(z), 
        4*cos(1/8*x)*cos(y)*sin(z)))            

def createGeometry(n):
    structuredMeshUnitBrick = MakeStructured3DMesh(hexes=False, nx=n, ny=n, nz=n)
    return structuredMeshUnitBrick

results = []
for n in ns:
    mesh = createGeometry(n)
    for order in orders:
        u, p, ndofs, eX = nhl.hodgeLaplaceTwoForms3D(mesh, g, order, Cw)
        results.append({'h': 1/n, 'ndofs':ndofs, 'order':order, 'eX':eX})

df_oneForms2D = pd.DataFrame(results)
df_oneForms2D.to_csv("data/twoForms3Ddata.csv", index=False)