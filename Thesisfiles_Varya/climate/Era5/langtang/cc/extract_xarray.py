# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 15:28:44 2023

@author: leon
"""

import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
import glob

path = 'D:\\climatedata\\era5land\\langtang\\cc\\*.nc'
file = xr.open_mfdataset(path, combine='by_coords')

print(file.variables.keys())

lon_data = file.variables['longitude'][:]
print(lon_data)

lat_data = file.variables['latitude'][:]
print(lat_data)


gridcell = file.sel(latitude=28.4, longitude=85.7, method='nearest')
print(gridcell)

# select time
start_date = '1950-01-01T00:00:00.000000000'
end_date = '2023-12-31T23:00:00.000000000'
cut = gridcell.sel(time=slice(start_date, end_date))

# look at the data:
# convert to dataframe for convenience 
cutdf = cut.to_dataframe()
cutdf = cutdf.rename(columns={'tcc': 'N'})
cutdf.index.name = 'D'

cutdf[['N']].to_csv("D:\climatedata\merge\cc.csv")