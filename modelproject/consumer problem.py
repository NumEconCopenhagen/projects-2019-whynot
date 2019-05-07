#%%
import numpy as np
import scipy as sp
from scipy import linalg
from scipy import optimize
from scipy import interpolate
import sympy as sm

%matplotlib inline
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
#%%
sm.init_printing(use_unicode=True)

#%%
def utility(q1,q2,rho):
    return (q1**rho+q2**rho)**(1/rho)

def budgcons(q1,q2,p1,p2):
    return q1*p1+q2*p2

def consprob(q1,p1,p2,rho,Y):
    (q1**rho+((Y-q1*p1)/p2)**rho)**(1/rho)


