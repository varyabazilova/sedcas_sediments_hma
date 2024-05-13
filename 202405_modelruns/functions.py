
# functions for processing of the sedcas paper data, amd model outputs
# created by varyabazilova in May 2024 

# libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os






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
def calculate_monthly_sediment_yield_all(sediments, column):    
    ''' the output is in m3'''
    # Create DataFrame for sediments with area considered
    sediments_area = pd.DataFrame()
    sediments_area['D'] = pd.to_datetime(sediments.D)
    if column == 'Q100':
        sediments_area['Q100'] = sediments.Q100 * 4830.0
    if column == 'dfs':
        sediments_area['dfs'] = sediments.dfs * 4830.0
    if column == 'Qstl':
        sediments_area['Qstl'] = sediments.Qstl * 4830.0
    if column == 'Qdftl':
        sediments_area['Qdftl'] = sediments.Qdftl * 4830.0

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


def melted_df_for_boxplots_monthly(elevation_df, monthly_data, timestep_df, land_cover, column):
    '''
    df: dataframe with model output
    elevation: elevation table with cellnr2 and elevation/band_data 
    timestep_df: df with index, year and month number
    land_cover: string with land cover type
    column: column of interest from the output data
    '''
    elevation = elevation_df.transpose()
    elevation_list = elevation.loc['cellnr2'].tolist()
    # make columns in the correct order 
    monthly_data = monthly_data[elevation_list]
    # make sure its the same 
    # if elevation_list == df.columns.tolist():
    #     continie 
    # else: print('columns fo not match!') 
      # rename columns according the the elevation and merge with timestep 
    monthly_data.columns = elevation.loc['band_data']
    df = pd.concat([timestep_df, monthly_data],axis=1)
    df['land_cover'] = land_cover
    # melt table 
    melted = pd.melt(df, id_vars=['year', 'month', 'land_cover'], var_name='elevation', value_name=column)
    return melted


def melted_df_for_boxplots_monthly_mean(elevation, monthly_mean, land_cover, column):
    '''
    df: dataframe with model output
    elevation: elevation table with cellnr2 and elevation/band_data 
    land_cover: string with land cover type
    column: column of interest from the output data
    '''
    elevation = elevation.transpose()
    elevation_list = elevation.loc['cellnr2'].tolist()
    # make columns in the correct order 
    monthly_mean = monthly_mean[elevation_list]
    # rename columns 
    monthly_mean.columns = elevation.loc['band_data']
    # adjust month 
    monthly_mean['month'] = monthly_mean.index.values + 1
    monthly_mean['land_cover'] = land_cover
    # melt table 
    melted = pd.melt(monthly_mean, id_vars=['month', 'land_cover'], var_name='elevation', value_name=column)
    return melted


def bin_elevation(row):
    ''' function to create elevation bins''' 
    if row['elevation'] <2500:
        return '<2500'
    elif 2500 <= row['elevation'] < 3000:
        return '2500 - 3000'
    elif 3000 <= row['elevation'] < 3500:
        return '3000 - 3500'
    elif 3500 <= row['elevation'] < 4000:
        return '3500 - 4000'
    elif 4000 <= row['elevation'] < 4500:
        return '4000 - 4500'
    elif 4500 <= row['elevation'] < 5000:
        return '4500 - 5000'
    elif 5000 <= row['elevation'] < 5500:
        return '5000 - 5500'
    elif 5500 <= row['elevation'] < 6000:
        return '5500 - 6000'
    elif 6000 <= row['elevation'] :
        return '>6000'







# ------- archive functions -? 
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