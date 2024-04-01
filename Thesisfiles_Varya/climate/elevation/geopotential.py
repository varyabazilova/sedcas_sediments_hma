# -*- coding: utf-8 -*-
"""
Created on Thu Nov 2 15:07:08 2023

@author: leon
"""

import xarray as xr
import pandas as pd
import numpy as np

# Replace 'D:\geopotential.nc' with the path to your NetCDF file
file_path = r'D:\geopotential.nc'

# Open the NetCDF file using xarray
ds = xr.open_dataset(file_path)

# Define the latitude and longitude ranges
min_lat = 35.8
max_lat = 36.2
min_lon = 74.3
max_lon = 74.8

# Create lists to store extracted data
data = []

# Initialize index
index = 1

# Iterate over latitude and longitude ranges
for target_lat in np.arange(min_lat, max_lat + 0.1, 0.1):  # Adjust the step size as needed
    for target_lon in np.arange(min_lon, max_lon + 0.1, 0.1):  # Adjust the step size as needed
        # Find the indices of the closest latitude and longitude in the dataset
        lat_idx = np.abs(ds['latitude'].values - target_lat).argmin()
        lon_idx = np.abs(ds['longitude'].values - target_lon).argmin()

        # Extract the data for the specified coordinate
        latitude_value = ds['latitude'].values[lat_idx]
        longitude_value = ds['longitude'].values[lon_idx]
        z_value = ds['z'].values[:, lat_idx, lon_idx].squeeze() / 9.80665  # Divide by 9.80665

        # Append values to the data list
        data.append([index, latitude_value, longitude_value, *z_value.flatten()])  # Include index
        index += 1  # Increment index

# Create a Pandas DataFrame from the list
df = pd.DataFrame(data, columns=['Index', 'Latitude', 'Longitude', 'Z'])

# Display the DataFrame
print(df)
