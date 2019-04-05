#%%
# Import of pandas and numpy for work and analysis on lists and arrays
import pandas as pd
import numpy as np
#%%
# import of matplot for making graphs later on in the analysis
import matplotlib.pyplot as plt
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
# We shorten down the list of data for later use to equal the data we get for real-estate prices
# Afterwards we reset the index numbers and rename the columns to better identify the data
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
# We run sample values of the variables to find the correct id's to fetch the right data we want to focus on
ejpris_vars['values'][0][:10]
ejpris_vars['values'][1][:10]
ejpris_vars['values'][2][:10]
ejpris_vars['values'][3][:]
#%%
# We create a dictionary of the id's and corresponding text for the years we need. We choose to focus on fourth quarter of each year
TIDID=ejpris_vars['values'][3][:]
K4=TIDID[3::4]
#%%
# We then create a list using a for loop of the id's we need for the input of time in the API call we will use later
K4id = []
for row in K4:
    K4id.append(row['id'])
K4id
#%%
# Lastly we use a for loop to convert the list into a string for the input in the API call
K4input=''
for year in K4id:
    K4input +=  year + ','
K4input
#%%
# As we now have the id's we need to fetch our data, we fetch the real-estate priceindex for the variables we have chosen
# Furthermore we rename columns to easily identify the variables
# We choose to focus on index-values for apartments in Copenhagen every fourth quarter of every year
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
# As we have the data we need in two dataframes, we concatenate the two dataframes in a single datafram
forprisindex
ejprisindex
samlet2015priser=pd.concat([ejprisindex,forprisindex], axis=1)
samlet2015priser
#%%
# We drop columns we don't need to keep the dataframe as simple as possible.
samlet2015priser = samlet2015priser.drop(["HOVED", "Year (average)"], axis=1)
samlet2015priser
#%%
# For the next step, we need to calculate new values based on existing values in the dataframe
# Therefore we investigate the types of each column in the dataframe
samlet2015priser.dtypes
#%%
# The index values for both apartment-prices and consumer-prices are strings and therefore wee need to convert them to floats
# We need to replace "," wil "." in the index values to have the right syntax in python before we can convert the values to floats
# Lastly we convert the two columns to floats
samlet2015priser['Priceindex for sold apartements (2006=100)'] = [x.replace(',', '.') for x in samlet2015priser['Priceindex for sold apartements (2006=100)']]
samlet2015priser['Consumerpriceindex (2015=100)'] = [x.replace(',', '.') for x in samlet2015priser['Consumerpriceindex (2015=100)']]
samlet2015priser['Priceindex for sold apartements (2006=100)']=samlet2015priser['Priceindex for sold apartements (2006=100)'].astype(float)
samlet2015priser['Consumerpriceindex (2015=100)']=samlet2015priser['Consumerpriceindex (2015=100)'].astype(float)
#%%
# Now we create a new column in which we rebase the index for apartment-prices to 2015 to match the consumerpriceindex
# Afterwards we create a new column with a deflated priceindex of the apartment-prices
samlet2015priser['Priceindex for sold apartements (2015=100)']=samlet2015priser['Priceindex for sold apartements (2006=100)']*100/113.8
samlet2015priser['Inflation adjusted priceindex']= samlet2015priser['Priceindex for sold apartements (2015=100)']/samlet2015priser['Consumerpriceindex (2015=100)']*100
samlet2015priser
#%%
# Next we load morgagebond rates from excel with data gotten form Finansdanmark
rates = pd.read_excel('Morgagebond_rates.xlsx', converters={'Year':int})
#%%
# We define a function for calculating the present value
def present_value(rate):
    """ The present value of a annuity. 
    Calulates the present value of a yearly payment of 1 kr. paid in 30 years at rate x.
    Args:
        rate (float): the rate
        
    Returns:
        present value of 1 kr. in 30 years at rate x
    """
    try:
        return (1 - (1 + rate/100)**-30)/rate/100 
        #return 1
    except:
        print('Error: Check input')
#%%
# We use the present value function to calculate the present value of a 30-year annuity
# We add a column to rates with the present_value of a 30-year annuity
rates['PV_Long_rates'] = present_value(rates['Long_rates'])
rates
#%%
# We create a new baseyear of 2015
base_year = rates.iloc[16, 3]

# We Add an index of PV with baseyear 2015
rates['Index'] = rates['PV_Long_rates'] / base_year * 100

rates
#%%
# We drop the last row in rates as we don't have this data in our samlet2015priser dataframe
rates=rates.iloc[:20,]
rates
#%%
# We drop thee first seven rows in samlet2015priser as we don't have this data in the rates dataframe
samlet2015priser=samlet2015priser.iloc[7:,]
samlet2015priser=samlet2015priser.reset_index(drop=True)
samlet2015priser
#%%
# We add the index column from rates to samlet2015priser
samlet2015priser['PV index (2015=100)']=rates['Index']
samlet2015priser
#%%
# We create a graph, plotting the lines for the adjusted apartment-price index and the present value index
plt.plot(samlet2015priser['Year (Q4)'], samlet2015priser['Inflation adjusted priceindex'], 'b-', label='Apart Index')
plt.plot(samlet2015priser['Year (Q4)'], samlet2015priser['PV index (2015=100)'], 'g-', label='PV Index')
plt.legend(loc='best')
plt.xticks(['1999K4','2003K4','2008K4','2013K4','2018K4'])
plt.ylabel('Percent')
plt.xlabel('Year')
plt.title('Apart vs PV index (2015=100')
plt.show()
#%%
# We calculate the correlation coeficcient
np.corrcoef(samlet2015priser['PV index (2015=100)'], samlet2015priser['Inflation adjusted priceindex'])
