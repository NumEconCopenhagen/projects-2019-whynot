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
def utility(x1,x2,rho):
    return (x1**rho+x2**rho)**(1/rho)

def budgcons(,2,p1,p2):
    return 
