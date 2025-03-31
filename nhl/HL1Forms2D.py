from ngsolve import *

def hodgeLaplaceOneForms2D(mesh,
                       g = None,    # this is the manufactured solution, when none is given we set it to the zero solution
                       order = 1,   
                       C_w = 1):    # Nitsche penalty parameter
    """Calculates the NitscheHodgeLaplace in 2D for 1-forms. Linear system solved with PARDISO"""
    
    from nhl.autoDiffFunctions import GDiv, GCurl, GGrad
    from nhl.util import L2errorVOL, L2errorBND
    
    if g is None:
        g = CF((0,0))

    H_curl = HCurl(mesh, order=order, type1=True)
    H_1 = H1(mesh, order=order)
    fes = H_1 * H_curl
    (p, u), (q, v) = fes.TnT()

    n = specialcf.normal(mesh.dim)
    h = specialcf.mesh_size
    t = specialcf.tangential(mesh.dim)
    dS = ds(skeleton=True, definedon=mesh.Boundaries(".*"))

    f = CF(GCurl(GCurl(g, mesh), mesh) - GGrad(GDiv(g), mesh))                             
        
    gamma_n_u = -curl(u)*t
    gamma_n_v = -curl(v)*t

    gamma_p_v = v - n*(v*n)
    gamma_p_u = u - n*(u*n)
    gamma_p_g = g - n*(g*n)

    B, F  = BilinearForm(fes), LinearForm(fes)

    B +=  curl(u) * curl(v) * dx
    B +=  grad(p) * v * dx
    B += u * grad(q) * dx
    B += - p * q * dx

    B += gamma_n_v * gamma_p_u * dS
    B += gamma_p_v * gamma_n_u * dS
    B += (C_w/h) * gamma_p_v * gamma_p_u * dS

    F += f * v * dx
    F +=  (C_w / h) * gamma_p_g * gamma_p_v * dS
    F +=  gamma_n_v * gamma_p_g * dS
    F +=  (g*n) * q * ds
    
    with TaskManager(): 
        B.Assemble()
        F.Assemble()
        sol = GridFunction(fes)
        res = F.vec-B.mat * sol.vec
        inv = B.mat.Inverse(freedofs=fes.FreeDofs(), inverse="pardiso")
    
    sol.vec.data += inv * res
    
    gf_p , gf_u = sol.components

    # Computation of all quantities needed to derive the error in the X-norm
    curl_u = curl(gf_u)
    grad_p = grad(gf_p)
    curl_g = CF(GCurl(g, mesh))
    p_m = - CF(GDiv(g))                                             # Computation of p
    grad_p_m = CF(GGrad(p_m, mesh))
    gf_gamma_p_u = CF((gf_u - n*(gf_u*n)))                          # Gamma parallel
    gf_gamma_p_g = CF((g - n*(g*n)))
    gf_gamma_n_u = BoundaryFromVolumeCF(curl_u)                     # Gamma n
    gf_gamma_n_g = BoundaryFromVolumeCF(curl_g)
    h_avg = 1 / Integrate(1, mesh, VOL) * Integrate(h, mesh, VOL)
    # Actual error evaluation
    # Computation of L2 errors in the volume
    E_u = L2errorVOL(gf_u, g, mesh)
    E_curl_u = L2errorVOL(curl_u, curl_g, mesh)
    E_H_curl_u = E_u + E_curl_u
    E_p = L2errorVOL(gf_p, p_m, mesh)
    E_grad_p = L2errorVOL(grad_p, grad_p_m, mesh)
    # Computation of L2 errors on the boundary
    E_gamma_p_u = L2errorBND(gf_gamma_p_u, gf_gamma_p_g, mesh)
    E_gamma_n_u = L2errorBND(gf_gamma_n_u, gf_gamma_n_g, mesh)
    # Hashtag and X Error norm
    HT_E_gamma_p_u = h_avg**(-1)*E_gamma_p_u
    HT_E_gamma_n_u = h_avg*E_gamma_n_u
    HT_E_u = E_H_curl_u + HT_E_gamma_p_u + HT_E_gamma_n_u
    E_h_grad_p = h_avg**2 * E_grad_p
    X_E_u_p = HT_E_u + E_p + E_h_grad_p
    
    return (gf_u, gf_p, fes.ndof, sqrt(X_E_u_p))