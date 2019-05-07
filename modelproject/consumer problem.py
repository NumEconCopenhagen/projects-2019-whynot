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
I = sm.symbols('I')

utility=(q1**rho+q2**rho)**(1/rho)
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

