import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, OptimizeWarning
import warnings
import nhl # Import the Nitsche Hodge Laplace package for the fit_reference_line function

def reference_line_func(h_values, scaling_factor, slope):
    """This function is a helper function used by fit_reference_line() to calculate the scaling factor and the slope (the convergence rate)"""
    return scaling_factor * h_values ** slope

def fit_reference_line(h_values, error_values):
    """This function computes scaling factor and the slope (or convergence rate) of the given h values"""
    with warnings.catch_warnings():                         # suppressing an annoying warning that says covariance cannot be estimated
        warnings.simplefilter("ignore", OptimizeWarning)
        popt, _ = curve_fit(reference_line_func, h_values, error_values, p0=[1, 1]) 

    scaling_factor, slope = popt
    return scaling_factor, slope

df1f2D = pd.read_csv('data/oneForms2Ddata.csv')
df1f3D = pd.read_csv('data/oneForms3Ddata.csv')
df2f3D = pd.read_csv('data/twoForms3Ddata.csv')

def plot_ex_vs_h(df, title, pdf_filename):
    line_width = 2
    orders = sorted(df['order'].unique())
    
    plt.figure(figsize=(8, 6))
    for order in orders:
        df_order = df[df['order'] == order].copy()
        h_values = df_order['h'].values
        error_values = df_order['eX'].values
        plt.loglog(h_values, error_values, marker='o', linewidth=line_width, 
                 label=f'Order {int(order)}')
        if len(h_values) >= 2:
            h_fit_values = h_values[-2:]
            error_fit_values = error_values[-2:]
            try:
                scaling_factor, slope = fit_reference_line(h_fit_values, error_fit_values)
                ref_values = scaling_factor * (h_values ** slope)
                plt.loglog(
                    h_values, 
                    ref_values, 
                    linestyle='dashdot', 
                    color='gray',
                    linewidth=(line_width - 1),
                    label=f"$O(h^{{{slope:.2f}}})$"
                )
            except RuntimeError as e:
                print(f"Warning: Slope fit failed for order {order} with error: {e}")
    
    plt.xlabel('h')
    plt.ylabel(r'$\| x - x_h \|_{X}$')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig(pdf_filename, format='pdf')
    plt.close()

title1 = "2D 1-form experiments on the unit square \n" +  r"$x_h = (\mathbf{u}_h, p_h) \subset V_h^{ND1} \times V_h^{CG}, \quad \| (\mathbf{u}_h, p_h) \|_X = \| \mathbf{u}_h \|_{\#} + \| p_h \| + h \| \nabla p_h \|.$"
title2 = "3D 1-form experiments on the unit brick \n" +  r"$x_h = (\mathbf{u}_h, p_h) \subset V_h^{ND1} \times V_h^{CG}, \quad \| (\mathbf{u}_h, p_h) \|_X = \| \mathbf{u}_h \|_{\#} + \| p_h \| + h \| \nabla p_h \|.$"
title3 = "3D 2-form experiments on the unit brick \n" +  r"$x_h = (\mathbf{u}_h, \mathbf{p}_h) \subset V_h^{RT} \times V_h^{ND1}, \quad \| (\mathbf{u}_h, \mathbf{p}_h) \|_X = \| \mathbf{u}_h \|_{\#} + \| \mathbf{p}_h \| + h \| \nabla \cdot \mathbf{p}_h \|.$"
plot_ex_vs_h(df1f2D, title1, "plots/oneForms2D.pdf")
plot_ex_vs_h(df1f3D, title2, "plots/oneForms3D.pdf")
plot_ex_vs_h(df2f3D, title3, "plots/twoForms3D.pdf")