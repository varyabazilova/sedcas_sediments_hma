import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob

# Common Coordinates
latitude = 36.1
longitude = 74.8

# Function to load and preprocess data
def load_and_process_data(path, variable_name, output_filename, column_name, start_date, end_date):
    # Load dataset
    file = xr.open_mfdataset(path, combine='by_coords')

    # Display variable keys
    print(file.variables.keys())

    # Select grid cell
    gridcell = file.sel(latitude=latitude, longitude=longitude, method='nearest')
    print(gridcell)

    # Select time range
    cut = gridcell.sel(time=slice(start_date, end_date))

    # Convert to DataFrame for convenience
    cutdf = cut.to_dataframe()
    cutdf = cutdf.rename(columns={variable_name: column_name})
    cutdf.index.name = 'D'

    # Save to CSV
    cutdf[[column_name]].to_csv(output_filename)

# Solar radiation data
path_swr = 'D:\\climatedata\\era5land\\bagrot\\swr\\*.nc'
load_and_process_data(path_swr, 'ssrd', r'D:\climatedata\merge\Rsw.csv', 'Rsw', '1951-09-01', '2022-09-30')

# Temperature data
path_temp = 'D:\\climatedata\\era5land\\bagrot\\temp\\*.nc'
load_and_process_data(path_temp, 't2m', r'D:\climatedata\merge\Ta.csv', 'Ta', '1951-01-01', '2023-12-31')

# Cloud cover data
path_cc = 'D:\\climatedata\\era5land\\bagrot\\cc\\*.nc'
load_and_process_data(path_cc, 'tcc', r'D:\climatedata\merge\cc.csv', 'N', '1950-01-01', '2023-12-31')

# Precipitation data
path_pr = 'D:\\climatedata\\era5land\\bagrot\\precipitation\\*.nc'
load_and_process_data(path_pr, 'tp', r'D:\climatedata\merge\Pr.csv', 'Pr', '1950-01-01', '2023-12-31')
