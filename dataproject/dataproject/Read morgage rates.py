#%%
# Import of pandas and numpy for work and analysis on lists and arrays
import pandas as pd
import numpy as np

#import custom present_value function
from present_value_function import present_value
#%%
# import of matplot for making graphs later on in the analysis
import matplotlib.pyplot as plt

#%%
#load rates from excel
rates = pd.read_excel('Morgagebond_rates.xlsx', converters={'Year':int})

#%%
#add column to rates with the present_value of a 30-year annuity
rates['PV_Long_rates'] = present_value(rates['Long_rates'])

#selecting base year
#Should be changed to .loc but will not accept .loc('2009',:)
#%%
base_year = rates.iloc[10, 3]

#Addting index of PV as index with base 2009
rates['Index'] = rates['PV_Long_rates'] / base_year * 100

print(rates)

#%%
x = rates['Year']
y = rates['Index']
plt.plot(x, y)
plt.show



