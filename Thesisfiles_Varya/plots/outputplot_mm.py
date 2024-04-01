# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 10:54:12 2023

@author: leon
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

#%matplotlib inline

# Specify the directory containing the .out files
directory = r"D:\outputs_sedcas\Mustang\[0.1478,0.7802,0.072]\sed"

# Get a list of all files with a .out extension in the directory
out_files = [file for file in os.listdir(directory) if file.endswith('.out')]

# Sort the out_files list based on the file numbers
out_files.sort(key=lambda x: int(x.split('.')[1].split('.')[0]))

# Initialize a DataFrame to accumulate Qdftl values
combined_df = pd.DataFrame()

# Iterate over each .out file
for out_file in out_files:
    # Extract the number between two underscores from the filename
    file_number = out_file.split('.')[1].split('.')[0]

    # Construct the full path to the current file
    file_path = os.path.join(directory, out_file)

    # Read the sediment data from a CSV file and convert it to a DataFrame
    path = pd.read_csv(file_path, index_col=0)
    sediments = path

    # Set the desired time frame
    start_date = '1986-09-01T00:00:00.000000000'
    end_date = '2022-09-30T23:00:00.000000000'

    # Convert the 'D' index to datetime
    sediments.index = pd.to_datetime(sediments.index)

    # Filter the DataFrame based on the desired time frame
    sediments = sediments[(sediments.index >= start_date) & (sediments.index <= end_date)]

    # Creating a new DataFrame
    sediments_area = pd.DataFrame()
    sediments_area['Qstl'] = sediments.Qstl
    sediments_area['Qdftl'] = sediments.Qdftl
    sediments_area.index = pd.to_datetime(sediments_area.index)

    # Resampling data to monthly frequency and calculating monthly means
    sym = sediments_area.resample('m').sum()
    symm_westernhimal = sym.groupby(by=sym.index.month).mean()
    symm_westernhimal = symm_westernhimal.reset_index()

    # Append Qdftl values to the combined DataFrame
    combined_df[file_number] = symm_westernhimal['Qdftl']


# List of month abbreviations
month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Plotting combined Qdftl values from all files without markers
fig_combined, ax_combined = plt.subplots(figsize=(12, 8))
combined_df.plot(ax=ax_combined, linestyle='-', markersize=8, legend=False)

ax_combined.set_xticks(range(0, len(combined_df.index)))
ax_combined.set_xticklabels([month_labels[i % 12] for i in range(len(combined_df.index))], rotation=45, ha='right')

ax_combined.set_xlabel('Months', fontsize=32)
ax_combined.set_ylabel('Debris flow yield (mm/month)', fontsize=32)
ax_combined.set_title('1986-2022', fontsize=36)
ax_combined.tick_params(axis='both', labelsize=28)
ax_combined.set_ylim(0, 80)
fig_combined.tight_layout()

# Save the combined figure
fig_combined.savefig('combined_sed_yeld_Qdftl_mm.pdf', bbox_inches='tight')

# Calculate percentiles (10th, 25th, 50th/median, 75th, 90th) of Qdftl values across all files for each month
percentiles = combined_df.quantile([0.1, 0.25, 0.5, 0.75, 0.9], axis=1)

# Plotting the percentiles of Qdftl values across all files with shaded areas
fig_percentiles, ax_percentiles = plt.subplots(figsize=(10, 6))

# Plotting the median line
percentiles.loc[0.5].plot(ax=ax_percentiles, linestyle='-', marker='', markersize=8, label='Median')

# Filling the space between 90th and 10th percentiles with transparent color
ax_percentiles.fill_between(percentiles.columns, percentiles.loc[0.1], percentiles.loc[0.9], color='lightblue', alpha=0.5, label='10th-90th Percentile')

# Filling the space between 75th and 25th percentiles with transparent color
ax_percentiles.fill_between(percentiles.columns, percentiles.loc[0.25], percentiles.loc[0.75], color='lightcoral', alpha=0.5, label='25th-75th Percentile')

ax_percentiles.set_xticks(range(0, len(percentiles.columns)))
ax_percentiles.set_xticklabels([month_labels[i % 12] for i in range(len(percentiles.columns))], rotation=45, ha='right')

ax_percentiles.set_xlabel('Months', fontsize=15)
ax_percentiles.set_ylabel('Qdftl (mm)', fontsize=15)
ax_percentiles.set_title('Percentiles of Qdftl Across Files Over Time', fontsize=18)
ax_percentiles.legend(fontsize=12)
ax_percentiles.tick_params(axis='both', labelsize=12)
ax_percentiles.set_ylim(0, 140)
fig_percentiles.tight_layout()

# Save the percentiles figure
fig_percentiles.savefig('percentiles_sed_yeld_Qdftl_filled_mm.pdf', bbox_inches='tight')

# Calculate average, max, and min values across all files for each month
average_max_min = pd.DataFrame({
    'Average': combined_df.mean(axis=1),
    'Max': combined_df.max(axis=1),
    'Min': combined_df.min(axis=1)
})

# Plotting the average, max, and min values across all files
fig_average_max_min, ax_average_max_min = plt.subplots(figsize=(10, 6))

# Plotting the average line
average_max_min['Average'].plot(ax=ax_average_max_min, linestyle='-', marker='', markersize=8, label='Average')

# Filling the space between max and min values with transparent color
ax_average_max_min.fill_between(average_max_min.index, average_max_min['Min'], average_max_min['Max'], color='lightgreen', alpha=0.5, label='Min-Max Range')

ax_average_max_min.set_xticks(range(0, len(average_max_min.index)))
ax_average_max_min.set_xticklabels([month_labels[i % 12] for i in range(len(average_max_min.index))], rotation=45, ha='right')

ax_average_max_min.set_xlabel('Months', fontsize=15)
ax_average_max_min.set_ylabel('Qdftl (mm)', fontsize=15)
ax_average_max_min.set_title('Average, Max, and Min Qdftl Across Files Over Time', fontsize=18)
ax_average_max_min.legend(fontsize=12)
ax_average_max_min.tick_params(axis='both', labelsize=12)
ax_average_max_min.set_ylim(0, 140)
fig_average_max_min.tight_layout()

# Save the average, max, min figure
fig_average_max_min.savefig('average_max_min_sed_yeld_Qdftl_filled_mm.pdf', bbox_inches='tight')

# Display the combined, percentiles, and average-max-min plots
plt.show()
