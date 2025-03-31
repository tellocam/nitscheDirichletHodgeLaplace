from ngsolve import *
from ngsolve.solvers import GMRes

def hodgeLaplaceTwoForms3D(mesh,
                       g = None,
                       order = 1,
                       C_w = 1):
    """Calculates the NitscheHodgeLaplace in 3D for 2-forms. Linear system solved with GMRes"""
    
    from nhl.autoDiffFunctions import GDiv, GCurl, GGrad
    from nhl.util import L2errorVOL, L2errorBND
    
    if g is None:
        g = CF((0,0,0))

    H_curl = HCurl(mesh, order=order, type1=True)
    H_div = HDiv(mesh, order=order-1, RT=True)
    fes = H_curl * H_div
    (p, u), (q, v) = fes.TnT()

    n = specialcf.normal(mesh.dim)
    h = specialcf.mesh_size
    dS = ds(skeleton=True, definedon=mesh.Boundaries(".*"))
    f = CF(GCurl(GCurl(g, mesh), mesh) - GGrad(GDiv(g), mesh))                             
        
    B, F  = BilinearForm(fes), LinearForm(fes)

    B += curl(p) * v * dx
    B += div(u) * div(v) * dx
    B += curl(q) * u * dx
    B += - p * q * dx

    B += - div(u) * (v*n) * dS
    B += - div(v) * (u*n) * dS
    B += (C_w/h) * (v*n) * (u*n) * dS

    F += f * v * dx
    F += - div(v) * (g*n) * dS
    F +=  (C_w/h) * (g*n) * (v*n) * dS
    F += Cross(n, q) * g * dS
    
    with TaskManager(): 
        B.Assemble()
        F.Assemble()
        sol = GridFunction(fes)
        blocks = fes.CreateSmoothingBlocks()
        prebj = B.mat.CreateBlockSmoother(blocks)
        GMRes(A =B.mat,x= sol.vec, b=F.vec,pre = prebj,  printrates="\r", maxsteps = 10000, tol=1e-8)

    gf_p , gf_u = sol.components

    # Computation of all quantities needed to derive errors
    div_u = div(gf_u)
    curl_p = curl(gf_p)
    div_g = CF(GDiv(g))
    p_m =  CF(GCurl(g, mesh))
    curl_p_m = CF(GCurl(p_m, mesh))

    div_u_bnd = BoundaryFromVolumeCF(div_u)
    div_g_bnd = BoundaryFromVolumeCF(div_g)

    gf_gamma_u_n = CF(gf_u * n)
    gf_gamma_g_n = CF(g * n)

    h_avg = 1 / Integrate(1, mesh, VOL) * Integrate(h, mesh, VOL)
    # Actual error evaluation
    # Computation of L2 errors in the volume
    E_u = L2errorVOL(gf_u, g, mesh)
    E_div_u = L2errorVOL(div_u, div_g, mesh)
    E_H_div_u = E_u + E_div_u
    E_p = L2errorVOL(gf_p, p_m, mesh)
    E_curl_p = L2errorVOL(curl_p, curl_p_m, mesh)
    # Computation of L2 errors on the boundary
    E_gamma_u_n = L2errorBND(gf_gamma_u_n, gf_gamma_g_n, mesh)
    E_gamma_div_u = L2errorBND(div_u_bnd, div_g_bnd, mesh)
    # Hashtag and X Error norm
    HT_E_gamma_u_n = h_avg**(-1)*E_gamma_u_n
    HT_E_gamma_div_u = h_avg*E_gamma_div_u
    HT_E_u = E_H_div_u + HT_E_gamma_u_n + HT_E_gamma_div_u
    E_h_curl_p = h_avg**2 * E_curl_p
    X_E_u_p = HT_E_u + E_p + E_h_curl_p

    return (gf_u, gf_p, fes.ndof, sqrt(X_E_u_p))