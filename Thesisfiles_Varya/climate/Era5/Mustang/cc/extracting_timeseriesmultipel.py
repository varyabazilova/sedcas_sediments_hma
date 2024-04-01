# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 11:45:30 2023

@author: leon
"""

import glob
from netCDF4 import Dataset
import pandas as pd
import numpy as np

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

#print(data.variables.keys()) use this line to check data    
###making an empty data frame change Temperature to the title of you collum
year_start = min(all_years)
year_end = max(all_years)
date_range = pd.date_range(start = year_start +"-01-01 00:00:00", end = year_end +'-12-31 23:00:00', freq = 'H')
df = pd.DataFrame(0.0, columns = ['N'], index = date_range)
df.index.name = 'D'

all_years.sort()

for yr in all_years:
    #reading in the data
    data = Dataset(str(yr)+'.nc','r')
    
    lat = data.variables['latitude'][:]
    lon = data.variables['longitude'][:]
    
    #accessing data make sure you acces the right data t2m is for temperature change temp to right variable
    temp = data.variables['tcc']
    
    start = str(yr) + '-01-01 00:00:00'
    end = str(yr) + '-12-31 23:00:00'
    d_range = pd.date_range(start = start, end = end, freq = 'H')
    #for df.loc change temp to right variable see comment above and change Temperature to richt name 
    for t_index in np.arange(0, len(d_range)):
        print('Recording the value for:' + str(d_range[t_index]))
        df.loc[d_range[t_index]]['N']= temp[t_index, 2, 1]
#change temperature to right name for data        
df.to_csv('D:\climatedata\merge\cc.csv', index = True)