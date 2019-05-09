#%%
import numpy as np
import scipy as sp
from scipy import linalg
from scipy import optimize
from scipy import interpolate
import sympy as sm
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
#%%
sm.init_printing(use_unicode=True)

#%%
q1 = sm.symbols('q_1')
q2 = sm.symbols('q_2')
p1 = sm.symbols('p_1')
p2 = sm.symbols('p_2')
rho = sm.symbols('rho')
mu = sm.symbols('mu')
I = sm.symbols('I')
U= sm.symbols('U')

#%%
utility=(q1**rho+q2**rho)**(1/rho)
utility

#%%
utility=sm.Eq(q1**rho*q2**mu,U)
utility
#%%
budgcons=sm.Eq(p1*q1+p2*q2,I)
budgcons
#%%
indiff=sm.solve(utility,q2)
indiff
#%%
q2_iso=sm.solve(budgcons,q2)
q2_iso
#%%
def find_opt(p1,p2,I,rho,mu):
#%%
util_subs=utility.subs(q2,q2_iso[0])
util_subs
#%%
foc=sm.diff(util_subs,q1)
foc
#%%
sol = sm.solve(sm.Eq(foc,0),q1)
sol
#%%
rho = 0.8
mu = 0.2
p1, p2 = 0.5, 1
I = 100

pmin, pmax = 0.5, 4
Imin, Imax = 10, 200
qmax = (3/4)*Imax/pmin

#%%
def consume_plot(p1=p1,p2=p2,I=I,rho=rho,mu=mu):
    
    q1 = np.linspace(0.1,qmax,num=100)
    q1e, q2e, uebar = sol(p1, p2 ,I, rho,mu)
    idfc = indiff(q1, uebar, rho, mu)
    budg = budgcons(q1, p1, p2, I)

    fig, ax = plt.subplots(figsize=(8,8))
    ax.plot(q1, budg, lw=2.5)
    ax.plot(q1, idfc, lw=2.5)
    ax.vlines(q1e,0,q2e, linestyles="dashed")
    ax.hlines(q2e,0,q1e, linestyles="dashed")
    ax.plot(q1e,q2e,'ob')
    ax.set_xlim(0, qmax)
    ax.set_ylim(0, qmax)
    ax.set_xlabel(r'$c_1$', fontsize=16)
    ax.set_ylabel('$c_2$', fontsize=16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.grid()
    plt.show()
#%%
consume_plot()
#%%
_sol_func = sm.lambdify((p1,I,rho,mu),sol[0])
def sol_func(p1,I=10,rho=1,mu=1):
    return _sol_func(p1,I,rho,mu)
    
# test
p1_vec = np.array([1.2,3,5,9])
demand_p1 = sol_func(p1_vec)
print(demand_p1)

