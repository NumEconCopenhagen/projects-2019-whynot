#%%
import numpy as np
import scipy as sp
from scipy import linalg
from scipy import optimize
from scipy import interpolate
import sympy as sm
import matplotlib.pyplot as plt
import math
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
#%%
def util(q1,q2,alpha):
    return (q1**alpha*q2**(1-alpha))

def budgcons(q1,p1,p2,I):
    return (I/p2)-(p1/p2)*q1

def indiff(q1,u,alpha):
    return (u/(q1**alpha))**(1/(1-alpha))
#%%
def optimum(p1,p2,I,alpha):
    q1=alpha*I/p1
    q2=(1-alpha)*I/p2
    u=util(q1,q2,alpha)
    return q1, q2, u
#%%
alpha = 0.8
p1, p2 = 1, 1
I = 100

pmin, pmax = 1, 4
Imin, Imax = 10, 200
qmax = (3/4)*Imax/pmin
#%%
def consume_plot(p1=p1, p2=p2, I=I, alpha=alpha):

    q1 = np.linspace(0.1,qmax,num=100)
    q1e, q2e, u = optimum(p1, p2 ,I, alpha)
    idfc = indiff(q1,u, alpha)
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
def optimum(p1,p2,I):
    q1= (I*p1+I*math.sqrt(p1*p2))/(p1**2-p1*p2)
    q2= -(I*p2+I*math.sqrt(p1*p2))/(p1*p2-p2**2)
    u=util(q1,q2)
    return q1, q2, u