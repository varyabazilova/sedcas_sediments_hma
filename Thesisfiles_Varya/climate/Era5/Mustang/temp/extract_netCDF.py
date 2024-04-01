# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 21:16:12 2023

@author: leon
"""

from netCDF4 import Dataset
import numpy as np
import glob

### Reading in the netCDF file
data = Dataset(r'1977.nc','r')
#print(data)

### Displaying the variables
print(data.variables.keys())

### Accessing the variables
#cc = data.variables['cc']
#print(cc)

### Acessing the data from the variables
time_data = data.variables['time'][:]
print(time_data)

lon_data = data.variables['longitude'][:]
print(lon_data)

lat_data = data.variables['latitude'][:]
print(lat_data)

temp_data = data.variables['t2m']
print(temp_data)

cc_data = data.variables['cc']
print(cc_data)
#cc_data = data.variables['cc'][:]
#print(cc_data)