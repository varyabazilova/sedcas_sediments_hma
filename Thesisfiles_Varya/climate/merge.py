# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 11:29:58 2023

@author: leon
"""

import pandas as pd
import glob

# Replace these with the paths to your CSV files

precipitation_file = 'HPr.csv'
temperature_file = 'Ta.csv'
swr_file = 'Rsw.csv'
cc_file = 'cc.csv'

precipitation_df = pd.read_csv(precipitation_file)
temperature_df = pd.read_csv(temperature_file)
swr_df = pd.read_csv(swr_file)
cc_df = pd.read_csv(cc_file)

# Convert temperature from Kelvin to Celsius
temperature_df['Ta'] = temperature_df['Ta'] - 273.15

cc_df['N'] = cc_df['N'].apply(lambda x: 1 if x > 1 else x)
cc_df['N'] = cc_df['N'].apply(lambda x: 0 if x < 0.001 else x)
cc_df['N'] = cc_df['N'].replace(0.0000152596040070562, 0)


precipitation_df['Pr'] = precipitation_df['Pr'].apply(lambda x: 0 if x < 0 else x)
precipitation_df['Pr'] = precipitation_df['Pr']*1000

swr_df['Rsw'] = swr_df['Rsw'].apply(lambda x: 0 if x < 0 else x)
swr_df['Rsw'] = swr_df['Rsw']/3600   ### Rsw era5 is in j/m2 and the model needs w/m2

merged_df = pd.merge(precipitation_df, temperature_df, on='D')

merged_df = pd.merge(merged_df, swr_df, on='D')
merged_df = pd.merge(merged_df, cc_df, on='D')


# Set 'D' as the index
merged_df.set_index('D', inplace=True)


merged_file = 'merged_data.csv'
merged_df.to_csv(merged_file, index=True)

merged_file_met = "D:\\climatedata\\merge\\mustang\\climatecell.88.met"
merged_df.to_csv(merged_file_met, index=True)

print(f'Merged data saved to {merged_file}')