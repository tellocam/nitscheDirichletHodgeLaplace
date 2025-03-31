from ngsolve import *

def L2errorVOL(u, u_h, mesh, c=1):
    """Function to compute the L2 error in the volume, c=1 by default"""
    errorVOL = Integrate(c*(u - u_h)**2*dx, mesh)
    return errorVOL

def L2errorBND(u, u_h, mesh, c=1):
    """Function to compute the L2 error on the boundary with skeleton=True, c=1 by default"""
    dS = ds(skeleton =True, definedon=mesh.Boundaries(".*"))
    errorBND = Integrate(c*(u - u_h)**2*dS, mesh)
    return errorBND