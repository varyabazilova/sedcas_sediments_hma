# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 16:04:11 2023

@author: leon
"""

import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
import glob

all_years = []
###reading all the years make sure .py is in same folder as data
for file in glob.glob('*.nc'):
    print(file)
    data = Dataset(file, 'r')
    time = data.variables['time']
    
    #listing the years make sure all the data has year.nc
    file_front, file_extention = file.split('.')
    year = file_front
    all_years.append(year)
    
#path = 'D:\climatedata\era5land\precipitation\*.nc'
#file = xr.open_mfdataset(path, combine='by_coords')
path = 'D:\\climatedata\\era5land\\precipitation\\'

for yr in all_years:    
    file = xr.open_dataset(str(yr) + '.nc')
    
    gridcell = file.sel(latitude=28.2, longitude=85.7, method='nearest')
    
    # select time
    start_date = str(yr) +'-01-01T00:00:00.000000000'
    end_date = str(yr) +'-12-31T23:00:00.000000000'
    cut = gridcell.sel(time=slice(start_date, end_date))
    
    # look at the data:
    # convert to dataframe for convenience 
    cutdf = cut.to_dataframe()
    
    # look at the dataframe
    cutdf.head()
    
    # look at the data: plot
    #plt.figure(figsize=(12, 6))
    #cut['tp'].plot.line(x='time', marker='o')
    #plt.grid(True)
    
    ''' you see that the precip accumulates and then resets in the end of each day, but what time does that happen - the max is in midnight'''
    
    print('max precip time:', cutdf.tp.idxmax())
    
    ''' we have to shift the precipitation one "step" back, so that max value occurs at 23:00, so that it is the same day '''
    
    shifted = cut.shift(time= -1, fill_value=0)
    
    ''' calculate the differences per hour within each day using shifted data ''' 
    
    # Create a sample xarray dataset for a year of data
    data = shifted
    
    # Function to calculate hourly differences with reset at midnight
    def calculate_hourly_diff(arr):
        diff = np.diff(arr, prepend=0)
        return xr.DataArray(diff, coords=arr.coords)
    
    # Calculate hourly differences with reset at midnight for the entire time series
    hourly_values = shifted.tp.groupby('time.dayofyear').apply(calculate_hourly_diff)
    
    # Create a new dataset with the hourly differences
    hourly_data = xr.Dataset({'hourly_values': hourly_values})
    
    ''' plot to see if its correct '''
    #plt.figure(figsize=(20, 6))
    #shifted['tp'].plot.line(x='time', marker='o', color ='lightblue', label ='original')
    hourly_data['hourly_values'].plot.line(x='time', marker='o', color ='orange', label = 'hourly')
    
    #plt.grid()
    #plt.legend()
    
    ''' calculate the sum within day in a shifted data, compare with the max within the same day in the original data '''
    
    # slice data - take a day  
    start_date = str(yr) +'-01-01T00:00:00.000000000'
    end_date = str(yr) +'-01-01T23:00:00.000000000'
    
    # Slice the dataset for a day 
    cut_sh = shifted.sel(time=slice(start_date, end_date))
    cut_hourl = hourly_data.sel(time=slice(start_date, end_date))
    
    print('new hourly data - daily sum:', round(cut_hourl.hourly_values.values.sum(), 6))
    print('original data - daily max (cumulative sum):', round(cut_sh.tp.values.max(), 6))
    
    ''' correct! '''
    
    # Since we shifted data, the last data point doesn't make sense anymore - cut it out
    #hourly_data = hourly_data.isel(time=slice(None, -1))
    
    # hourly_data - is the final dataset!!
    
    # Convert hourly_data to a Pandas DataFrame
    hourly_df = hourly_data.to_dataframe()
    
    # Rename the data column to 'Pr'
    hourly_df = hourly_df.rename(columns={'hourly_values': 'Pr'})
    
    # Give the index the name 'D'
    hourly_df = hourly_df.rename_axis('D')
    
    # Specify the path where you want to save the CSV file
    csv_file_path = 'D:\\climatedata\\era5land\\langtang\\Prextracted\\'+ str(yr)+'.csv'
    
    # Save the DataFrame to a CSV file with the named index and data column
    hourly_df.to_csv(csv_file_path, index=True)