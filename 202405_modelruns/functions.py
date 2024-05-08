
# functions for processing of the sedcas paper data, amd model outputs
# created by varyabazilova in May 2024 

# libraries
import pandas as pd
import matplotlib.pyplot as plt




# parameters
area = 4.83
# unit conversion
cf = (area * 10**6) * 10**-3  # km2 to m2 and mm to m

# functions

# sum per month, mean across years 
def calculate_monthly_sediment_yield(sediments):    
    ''' the output is in m3'''
    # Create DataFrame for sediments with area considered
    sediments_area = pd.DataFrame()
    sediments_area['D'] = pd.to_datetime(sediments.D)
    sediments_area['Q100'] = sediments.Q100 * 4830.0
    sediments_area['dfs'] = sediments.dfs * 4830.0

    sediments_area['Qstl'] = sediments.Qstl * 4830.0
    sediments_area['Qdftl'] = sediments.Qdftl * 4830.0

    # reset index to date
    sediments_area = sediments_area.set_index('D')

    # Resample to monthly and calculate sum
    sym = sediments_area.resample('m').sum()

    # Calculate monthly sediment yield mean
    symm_month = sym.groupby(by=sym.index.month).mean().reset_index()

    return symm_month

#  sum per month
def calculate_monthly_sediment_yield_all(sediments):    
    ''' the output is in m3'''
    # Create DataFrame for sediments with area considered
    sediments_area = pd.DataFrame()
    sediments_area['D'] = pd.to_datetime(sediments.D)
    sediments_area['Q100'] = sediments.Q100 * 4830.0
    # sediments_area['dfs'] = sediments.dfs * 4830.0

    # sediments_area['Qstl'] = sediments.Qstl * 4830.0
    # sediments_area['Qdftl'] = sediments.Qdftl * 4830.0

    # reset index to date
    sediments_area = sediments_area.set_index('D')

    # Resample to monthly and calculate sum
    sym = sediments_area.resample('m').sum()
    sym = sym.reset_index()
    sym['year'] = sym['D'].dt.year
    sym['month'] = sym['D'].dt.month

    # Calculate monthly sediment yield mean
    # symm_month = sym.groupby(by=sym.index.month).mean().reset_index()

    return sym





def convert_units_to_volume(sediments):
    # Create DataFrame for sediments with area considered
    sediments_area = pd.DataFrame()
    sediments_area['D'] = pd.to_datetime(sediments.D)
    sediments_area['Q100'] = sediments.Q100 * 4830.0
    # sediments_area['dfs'] = sediments.dfs * cf

    sediments_area['Qstl'] = sediments.Qstl * 4830.0
    sediments_area['Qdftl'] = sediments.Qdftl * 4830.0
    
    return sediments_area

def magnitude_frequency(sediments_area, column):
    """
    Calculate magnitude-frequency values for a column in a DataFrame.

    Parameters:
    - sediments_area (pandas.DataFrame): Input DataFrame.
    - column (str): Name of the column for which magnitude-frequency values are to be calculated.

    Returns:
    - pandas.DataFrame: DataFrame containing magnitude-frequency values.
    """
    # Copy the DataFrame to avoid modifying the original
    sediments_area = sediments_area.copy()
    
    # Sort data smallest to largest
    sediments_area = sediments_area[sediments_area[column] > 0]
    sediments_sorted = sediments_area.sort_values(by=column)

    # Count total observations
    n = sediments_sorted.shape[0]

    # Add a numbered column 1 -> n to use in return calculation for rank
    sediments_sorted.insert(0, 'rank', range(1, 1 + n))

    # Calculate probability - note you may need to adjust this value based upon the time period of your data
    sediments_sorted["prob"] = ((n - sediments_sorted["rank"] + 1) / (n + 1))

    sediments_sorted["return_period"] = (1 / sediments_sorted["prob"])

    return sediments_sorted

def add_elevation(elevation, df):
    ''' add elevation to the mean monthly data'''
    df = df.transpose()
    df = df.reset_index()
    df = df.rename(columns ={'index':'cellnr2'})
    merged = df.merge(elevation, on = 'cellnr2')
    return merged 


def data_for_boxplots_sorted(df, variable, sort_param):
    '''
    create a melted dataframe for boxplots
    df = dataframe 
    variebls = str(variable of interest)
    sort_params = str(how to sort)
    '''
    df = df.sort_values(sort_param)
    melted_df = pd.melt(df, id_vars=['cellnr2', 'band_data'], var_name='month', value_name= variable)
    return melted_df