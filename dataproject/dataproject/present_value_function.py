#%%
##Present value function
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



