#%%
# Import of pandas and numpy for work and analysis on lists and arrays
import pandas as pd
import numpy as np
#%%
# import of matplot for making graphs later on in the analysis
import matplotlib.pyplot as plt
#%%
#import custom present_value function
from present_value_function import present_value
#%%
# import of dst API functions. Note: requires installation of pip install git+https://github.com/elben10/pydst in terminal(mac)/cmd(windows)
import pydst
Dst = pydst.Dst(lang='da')
#%%
# Fetching variables for the consumer price index in dst
forpris_vars = Dst.get_variables(table_id='PRIS112')
forpris_vars
#%%
# Fetching data for the yearly average consumer price index with 2005=100
forprisindex = Dst.get_data(table_id = 'PRIS112', variables={'HOVED':['1005'], 'tid':['*']})
forprisindex
#%%
forprisindex=forprisindex.iloc[12:,]
forprisindex=forprisindex.reset_index(drop=True)
forprisindex.rename(
    columns={
        "TID": "Year (average)",
        "INDHOLD": "Consumerpriceindex (2015=100)"
    },
    inplace=True
)
forprisindex
#%%
# Fetching variables for the property price index in dst
ejpris_vars = Dst.get_variables(table_id='EJ55')
ejpris_vars
#%%
ejpris_vars['values'][0][:10]
ejpris_vars['values'][1][:10]
ejpris_vars['values'][2][:10]
ejpris_vars['values'][3][:]
#%%
TIDID=ejpris_vars['values'][3][:]
K4=TIDID[3::4]
#%%
K4id = []
for row in K4:
    K4id.append(row['id'])
K4id
#%%
K4input=''
for year in K4id:
    K4input +=  year + ','
K4input
#%%
ejprisindex = Dst.get_data(table_id = 'EJ55', variables={'OMRÅDE':['01'], 'EJENDOMSKATE':['2103'], 'TAL':['100'], 'Tid':[K4input]})
ejprisindex.rename(
    columns={
        "INDHOLD": "Priceindex for sold apartements (2006=100)",
        "TID": "Year (Q4)"
    },
    inplace=True
)
ejprisindex
#%%
forprisindex
ejprisindex
samlet2015priser=pd.concat([ejprisindex,forprisindex], axis=1)
samlet2015priser
#%%
samlet2015priser = samlet2015priser.drop(["HOVED", "Year (average)"], axis=1)
samlet2015priser
#%%
samlet2015priser.dtypes
#%%
samlet2015priser['Priceindex for sold apartements (2006=100)'] = [x.replace(',', '.') for x in samlet2015priser['Priceindex for sold apartements (2006=100)']]
samlet2015priser['Consumerpriceindex (2015=100)'] = [x.replace(',', '.') for x in samlet2015priser['Consumerpriceindex (2015=100)']]
samlet2015priser['Priceindex for sold apartements (2006=100)']=samlet2015priser['Priceindex for sold apartements (2006=100)'].astype(float)
samlet2015priser['Consumerpriceindex (2015=100)']=samlet2015priser['Consumerpriceindex (2015=100)'].astype(float)
#%%
samlet2015priser['Priceindex for sold apartements (2015=100)']=samlet2015priser['Priceindex for sold apartements (2006=100)']*100/113.8
samlet2015priser['Inflation adjusted priceindex']= samlet2015priser['Priceindex for sold apartements (2015=100)']/samlet2015priser['Consumerpriceindex (2015=100)']*100
samlet2015priser
#%%
#load rates from excel
rates = pd.read_excel('Morgagebond_rates.xlsx', converters={'Year':int})

#%%
#add column to rates with the present_value of a 30-year annuity
rates['PV_Long_rates'] = present_value(rates['Long_rates'])
rates
#selecting base year
#Should be changed to .loc but will not accept .loc('2015',:)
#%%
base_year = rates.iloc[16, 3]

#Addting index of PV as index with base 2015
rates['Index'] = rates['PV_Long_rates'] / base_year * 100

rates
#%%
rates=rates.iloc[:20,]
rates
#%%
samlet2015priser=samlet2015priser.iloc[7:,]
samlet2015priser=samlet2015priser.reset_index(drop=True)
samlet2015priser
#%%
samlet2015priser['PV index (2015=100)']=rates['Index']
samlet2015priser

#%%
x = rates['Year']
y = rates['Index']
plt.plot(x, y)
plt.show
#%%
plt.plot(samlet2015priser['Year (Q4)'], samlet2015priser['Inflation adjusted priceindex'], 'b-', label='Apart Index')
plt.plot(samlet2015priser['Year (Q4)'], samlet2015priser['PV index (2015=100)'], 'g-', label='PV Index')
plt.legend(loc='best')
plt.xticks(['1999K4','2003K4','2008K4','2013K4','2018K4'])
plt.ylabel('Percent')
plt.xlabel('Year')
plt.title('Apart vs PV index (2015=100')
plt.show()
#%%
np.corrcoef(samlet2015priser['PV index (2015=100)'], samlet2015priser['Inflation adjusted priceindex'])
