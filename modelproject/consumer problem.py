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

#%%
utility=(q1**rho+q2**rho)**(1/rho)
utility

#%%
utility=q1**rho*q2**mu
utility
#%%
budgcons=sm.Eq(p1*q1+p2*q2,I)
budgcons

#%%
q2_iso=sm.solve(budgcons,q2)
q2_iso

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
_sol_func = sm.lambdify((p1,I,rho,mu),sol[0])
def sol_func(p1,I=10,rho=0.8,mu=0.2):
    return _sol_func(p1,I,rho,mu)
    
# test
p1_vec = np.array([1.2,3,5,9])
demand_p1 = sol_func(p1_vec)
print(demand_p1)
