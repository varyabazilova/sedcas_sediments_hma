# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 11:39:26 2023

@author: leon
"""

import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

import glob

# read all data

directory = 'D:\\climatedata\\era5land\\langtang\\test\\'
files = glob.glob(directory + '*.nc')

# Use xarray.open_mfdataset to open and concatenate the .nc files
data = xr.open_mfdataset(files)
data = data.sortby('time')
# data['tp'] = data.tp * 1000 # check units

# shift 1 time step back 
data = data.shift(time= -1, fill_value=0).sortby('time')

# define function 
def calculate_hourly_diff(arr):
    diff = arr - arr.shift(time=1, fill_value=0)
    return xr.DataArray(diff, coords=arr.coords)

# apply function
hourly_values = data.tp.groupby('time.dayofyear').apply(calculate_hourly_diff)
hourly_data = xr.Dataset({'hourly_values': hourly_values})

''' calculate the sum within day in a shifted data, compare with the max within the same day in the original data '''
# slice coordinates
data = data.sel(latitude=29.0, longitude=84.0, method='nearest')
hourly_data = hourly_data.sel(latitude=29, longitude=84, method='nearest')

# slice data - take a day  
start_date = '2000-06-01T00:00:00.000000000'
end_date = '2000-06-01T23:00:00.000000000'

# Slice the dataset for a day 
cut_sh = data.sel(time=slice(start_date, end_date))
cut_hourl = hourly_data.sel(time=slice(start_date, end_date))

print('new hourly data - daily sum:', round(cut_hourl.hourly_values.values.sum(), 6))
print('original data - daily max (cumulative sum):', round(cut_sh.tp.values.max(), 6))