# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 17:03:03 2023

@author: leon
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Directory containing the debris flow output files for the first time period
folder_path_period1 = r"D:\outputs_sedcas\bagrot\[0.0755,0.6976,0.2269]\sed"

# Directory containing the debris flow output files for the second time period
folder_path_period2 = r"D:\outputs_sedcas\bagrot\[0.26,0.522,0.218]\sed"

# Create an empty list to store DataFrames for each time period
all_dfs_period1 = []
all_dfs_period2 = []

# Loop over all files in the folder for the first time period
for filename in os.listdir(folder_path_period1):
    if filename.endswith('.out'):  # Assuming all files have the .out extension
        # Full path to the current file
        file_path = os.path.join(folder_path_period1, filename)

        try:
            # Load the CSV file into a DataFrame
            df = pd.read_csv(file_path)

            # Check if the expected columns are present
            required_columns = ['D', 'z', 'Qdftl']
            if not set(required_columns).issubset(df.columns):
                raise ValueError(f"Missing required columns in file: {filename}")

            # Convert the 'D' column to datetime format
            df['D'] = pd.to_datetime(df['D'], format='%Y-%m-%d %H:%M:%S')

            # Extract the year and date (ignoring time) from the datetime column
            df['Year'] = df['D'].dt.year

            # Add the current dataframe to the list for the first time period
            all_dfs_period1.append(df)

        except Exception as e:
            print(f"Error processing file {filename}: {e}")

# Loop over all files in the folder for the second time period
for filename in os.listdir(folder_path_period2):
    if filename.endswith('.out'):  # Assuming all files have the .out extension
        # Full path to the current file
        file_path = os.path.join(folder_path_period2, filename)

        try:
            # Load the CSV file into a DataFrame
            df = pd.read_csv(file_path)

            # Check if the expected columns are present
            required_columns = ['D', 'z', 'Qdftl']
            if not set(required_columns).issubset(df.columns):
                raise ValueError(f"Missing required columns in file: {filename}")

            # Convert the 'D' column to datetime format
            df['D'] = pd.to_datetime(df['D'], format='%Y-%m-%d %H:%M:%S')

            # Extract the year and date (ignoring time) from the datetime column
            df['Year'] = df['D'].dt.year

            # Add the current dataframe to the list for the second time period
            all_dfs_period2.append(df)

        except Exception as e:
            print(f"Error processing file {filename}: {e}")

# Concatenate all dataframes in the list for each time period vertically
combined_df_period1 = pd.concat(all_dfs_period1, ignore_index=True)
combined_df_period2 = pd.concat(all_dfs_period2, ignore_index=True)

# Print the combined DataFrames for each time period
print("Combined DataFrame for Period 1:")
print(combined_df_period1)

print("Combined DataFrame for Period 2:")
print(combined_df_period2)

# Get user input for the time periods
start_year_period1 = 1951
end_year_period1 = 1986

start_year_period2 = 1986
end_year_period2 = 2022

# Define time periods for each DataFrame
time_period_1 = (combined_df_period1['Year'] >= start_year_period1) & (combined_df_period1['Year'] < end_year_period1)
time_period_2 = (combined_df_period2['Year'] >= start_year_period2) & (combined_df_period2['Year'] < end_year_period2)

# ... (previous code remains unchanged)

# ... (previous code remains unchanged)

# Filter DataFrames based on time periods and values greater than zero
filtered_df_period1 = combined_df_period1[(time_period_1) & (combined_df_period1['Qdftl'] > 0)].copy()
filtered_df_period1['Period'] = '1951-1986'

filtered_df_period2 = combined_df_period2[(time_period_2) & (combined_df_period2['Qdftl'] > 0)].copy()
filtered_df_period2['Period'] = '1986-2022'

# Print the filtered DataFrames for each time period
print(f"Filtered DataFrame for Period 1 ({start_year_period1}-{end_year_period1}):")
print(filtered_df_period1)

print(f"Filtered DataFrame for Period 2 ({start_year_period2}-{end_year_period2}):")
print(filtered_df_period2)

# ... (previous code remains unchanged)

# ... (previous code remains unchanged)

# Round 'z' column values in DataFrames and convert to integers
filtered_df_period1['z'] = filtered_df_period1['z'].round().astype(int)
filtered_df_period2['z'] = filtered_df_period2['z'].round().astype(int)

# Boxplot for both time periods in one plot with adjusted y-axis scaling
plt.figure(figsize=(12, 8))
sns.boxplot(x='z', y='Qdftl', hue='Period', data=pd.concat([filtered_df_period1, filtered_df_period2], ignore_index=True), showfliers=True, palette=['skyblue', 'lightcoral'])
plt.xlabel('Elevation (m)', fontsize = 32)
plt.ylabel('Debris Flow yield (mm/event)', fontsize = 30)
#plt.title('Debris Flow Output Comparison (Period 1 and Period 2)')
plt.xticks(rotation=45, fontsize=26)
plt.yticks(fontsize=26)
legend = plt.legend(title='Period', fontsize=26, loc='upper right')
legend.get_title().set_fontsize(26)
#plt.xticks(plt.xticks()[0][::3])
# Display the plot without gridlines
sns.despine()

plt.show()

# Continue with the same style for other plots...





# ... (continue with other plot types)

# ... (add other plots as needed)


# ... (continue with other plot types)

# ... (add other plots as needed)


# Violin plot for both time periods
plt.figure(figsize=(12, 6))
sns.violinplot(x='z', y='Qdftl', hue='Period', data=pd.concat([filtered_df_period1, filtered_df_period2], ignore_index=True), split=True, inner="quart", palette=['skyblue', 'lightcoral'])
plt.xlabel('Elevation (m)')
plt.ylabel('Debris Flow Output (Qdftl)')
plt.title('Debris Flow Output Comparison (Period 1 and Period 2)')
plt.xticks(rotation=45)
plt.legend(title='Period')
plt.show()

# Swarm plot for both time periods
plt.figure(figsize=(12, 6))
sns.swarmplot(x='z', y='Qdftl', hue='Period', data=pd.concat([filtered_df_period1, filtered_df_period2], ignore_index=True), palette=['skyblue', 'lightcoral'])
plt.xlabel('Elevation (m)')
plt.ylabel('Debris Flow Output (Qdftl)')
plt.title('Debris Flow Output Comparison (Period 1 and Period 2)')
plt.xticks(rotation=45)
plt.legend(title='Period')
plt.show()

# Point plot for both time periods
plt.figure(figsize=(12, 6))
sns.pointplot(x='z', y='Qdftl', hue='Period', data=pd.concat([filtered_df_period1, filtered_df_period2], ignore_index=True), ci="sd", palette=['skyblue', 'lightcoral'])
plt.xlabel('Elevation (m)')
plt.ylabel('Debris Flow Output (Qdftl)')
plt.title('Debris Flow Output Comparison (Period 1 and Period 2)')
plt.xticks(rotation=45)
plt.legend(title='Period')
plt.show()

# Scatter plot using stripplot for both time periods
plt.figure(figsize=(12, 6))
sns.stripplot(
    x='z',
    y='Qdftl',
    hue='Period',
    data=pd.concat([filtered_df_period1, filtered_df_period2], ignore_index=True),
    jitter=True,  # Add some jitter to separate points
    palette=['skyblue', 'lightcoral'],
    dodge=True  # Separate points for each period
)
plt.xlabel('Elevation (m)')
plt.ylabel('Debris Flow Output (Qdftl)')
plt.title('Scatter Plot: Debris Flow Output vs Elevation')
plt.xticks(rotation=45)
plt.legend(title='Period')
plt.show()
