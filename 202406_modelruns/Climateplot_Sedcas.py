# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 09:49:19 2024

@author: 6935737
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 3 10:45:22 2023
@author: leon
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

location = 'langtang'
# Path to the directory containing the files
# directory_path = "D:\\scriptie\\climatedata\\merge\\mustang"
directory_path = f'/Volumes/T7 Shield/202409_paper2_modelruns/May2025_30years/TL_data/2landcover/{location}_climate_cut'

# Get all subdirectories and find .met files in each
met_files = []
for item in os.listdir(directory_path):
    item_path = os.path.join(directory_path, item)
    if os.path.isdir(item_path):
        # Look for .met files in this subdirectory
        for file in os.listdir(item_path):
            if file.endswith(".met"):
                met_files.append(os.path.join(item, file))  
                # Store relative path

csv_files = met_files

# Define the date range for filtering
start_date = pd.to_datetime("1986-01-01")
end_date = pd.to_datetime("2022-12-31")

fig, ax1 = plt.subplots(figsize=(3.5, 2.5), dpi=600)

# Set font sizes
font_size_labels = 8
font_size_ticks = 7

ax1.set_xlabel('Month', fontsize=font_size_labels)
ax1.set_ylabel('Average Precipitation (mm)', color='tab:blue', fontsize=font_size_labels)

# Create a second y-axis for temperature
ax2 = ax1.twinx()
ax2.set_ylabel('Average Temperature (°C)', color='tab:red', fontsize=font_size_labels)

# Placeholder for overall average temperature and precipitation
overall_avg_temp = []
overall_avg_precip = []

# Lists to store individual temperature lines for filling
temp_lines = []

# Placeholder for individual precipitation data
all_precip_data = []

# Loop over each CSV file
for csv_file in csv_files:
    # Extract the number between the dots in the file name
    plot_number = ''.join(filter(str.isdigit, csv_file))

    # Construct the full path to the CSV file
    file_path = os.path.join(directory_path, csv_file)

    # Load your CSV data
    try:
        df = pd.read_csv(file_path)
    except UnicodeDecodeError as e:
         print(f"Error reading {csv_file}: {e}")
         df = pd.read_csv(file_path, encoding='latin-1')
         print(df)
    # Convert the 'D' column to datetime format and set it as the index
    df['D'] = pd.to_datetime(df['D'])
    
    # Filter data based on the specified date range
    df = df[(df['D'] >= start_date) & (df['D'] <= end_date)]

    # Set the filtered 'D' column as the index
    df.set_index('D', inplace=True)

    # Resample to monthly frequency and calculate mean temperature and sum of precipitation
    monthly_data = df.resample('M').agg({'Ta': 'mean', 'Pr': 'sum'})

    # Group by month and calculate average temperature and precipitation over the years
    average_monthly_data = monthly_data.groupby(monthly_data.index.month).agg({'Ta': ['mean', 'std'], 'Pr': ['mean', 'std']})

    # Plot the monthly average temperature and precipitation without error bars and markers
    ax1.bar(average_monthly_data.index, average_monthly_data['Pr']['mean'], alpha=0, color='tab:blue')

    # Plot individual temperature lines in gray without error bars and markers
    temp_line, = ax2.plot(average_monthly_data.index, average_monthly_data['Ta']['mean'], linestyle='-', color='tab:red', alpha=0,)

    # Save average temperature and precipitation data for later use
    overall_avg_temp.append(average_monthly_data['Ta']['mean'])
    overall_avg_precip.append(average_monthly_data['Pr']['mean'])
    
    # Save precipitation data for later use
    all_precip_data.append(average_monthly_data['Pr']['mean'])

    # Store the individual temperature line for filling
    temp_lines.append(temp_line)

# Calculate overall average temperature and precipitation
overall_avg_temp = pd.DataFrame(overall_avg_temp).mean()
overall_avg_precip = pd.DataFrame(overall_avg_precip).mean()

# Calculate the maximum and minimum precipitation values for each month
max_precip = pd.DataFrame(all_precip_data).max()
min_precip = pd.DataFrame(all_precip_data).min()

# Plot the overall average temperature line in a distinct color (e.g., red) without error bars and markers
overall_temp_line, = ax2.plot(overall_avg_temp.index, overall_avg_temp, linestyle='--', color='tab:red', label='Overall Avg Temp')

# Plot error bars to show the spread between the file with the most and least precipitation
precip_range = ax1.errorbar(overall_avg_precip.index, overall_avg_precip, yerr=[overall_avg_precip - min_precip, max_precip - overall_avg_precip], fmt='none', color='black', capsize=2, label='Precipitation Range')

# Extract maximum and minimum values from individual temperature lines
max_temp = pd.concat([pd.Series(line.get_ydata()) for line in temp_lines], axis=1).max(axis=1)
min_temp = pd.concat([pd.Series(line.get_ydata()) for line in temp_lines], axis=1).min(axis=1)

# Fill the area between the highest and lowest temperature lines with a red color
temp_range = ax2.fill_between(overall_avg_temp.index, max_temp, min_temp, color='tab:red', alpha=0.2, label='Temperature Range')

# Bar plot for overall average precipitation without error bars
avg_precip_bar = ax1.bar(overall_avg_precip.index, overall_avg_precip, alpha=0.7, color='tab:blue', label='Overall Avg Precip')

# Set y-axis limits for precipitation
ax1.set_ylim(0, 1000)  # Adjust the limit as needed

# Set y-axis limits for temperature
ax2.set_ylim(-30, 20)  # Adjust the limits as needed

# Adjust ticks font size
ax1.tick_params(axis='both', which='major', labelsize=font_size_ticks)
ax2.tick_params(axis='both', which='major', labelsize=font_size_ticks)

# Tight layout for compactness
plt.tight_layout()

# Save the plot as a high-resolution image
# output_file_path = os.path.join(directory_path, f"{location}.png")
output_file_path = f'/Users/varyabazilova/Desktop/paper2/plots_experiments/{location}.png'
plt.savefig(output_file_path, dpi=600, bbox_inches='tight')  # Save plot at 300 DPI

# Show the legend
#ax1.legend(handles=[avg_precip_bar, precip_range], loc='upper left', fontsize=font_size_ticks)
#ax2.legend(handles=[overall_temp_line, temp_range], loc='upper right', fontsize=font_size_ticks)

# Show the plot
plt.show()
