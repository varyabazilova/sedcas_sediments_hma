# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 17:03:03 2023

@author: leon
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Directory containing the hydro files
folder_path = r'D:\outputs_sedcas\mustang\era5_spatial\hydro'

# Create an empty list to store DataFrames
all_dfs = []

# Loop over all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.out'):  # Assuming all files have the .out extension
        # Full path to the current file
        file_path = os.path.join(folder_path, filename)

        try:
            # Load the CSV file into a DataFrame
            df = pd.read_csv(file_path)

            # Check if the expected columns are present
            required_columns = ['D', 'z', 'snow']
            if not set(required_columns).issubset(df.columns):
                raise ValueError(f"Missing required columns in file: {filename}")

            # Convert the 'D' column to datetime format
            df['D'] = pd.to_datetime(df['D'], format='%Y-%m-%d %H:%M:%S')

            # Extract the year and date (ignoring time) from the datetime column
            df['Year'] = df['D'].dt.year

            # Convert hourly snow data to daily snow presence (1 if snow is present at least once in the day, 0 otherwise)
            df['DailySnow'] = (df['snow'] > 0).groupby([df['Year'], df['D'].dt.date, df['z']]).transform('max')

            # Count the number of snow days per year and elevation (z) and divide by 24
            snowdays_per_elevation = df.groupby(['Year', 'z'])['DailySnow'].sum().reset_index()
            snowdays_per_elevation['DailySnow'] /= 24  # Divide by 24 to get the daily count

            # Add the current dataframe to the list
            all_dfs.append(snowdays_per_elevation)

        except Exception as e:
            print(f"Error processing file {filename}: {e}")

# Concatenate all dataframes in the list vertically
combined_df = pd.concat(all_dfs, ignore_index=True)

# Print the combined DataFrame
print(combined_df)

# Now you can use the combined_df for further analysis or plotting
# Convert 'z' column to integers (if not already)
combined_df['z'] = combined_df['z'].astype(int)

# Split the data into two time periods: 1951-1986 and 1986-2022
df_1951_1986 = combined_df[combined_df['Year'].between(1951, 1986)]
df_1986_2022 = combined_df[combined_df['Year'].between(1986, 2022)]

# Create a subplot with two boxplots
fig, axes = plt.subplots(1, 2, figsize=(18, 8), sharey=True)

# Subplot 1: 1951-1986
sns.boxplot(ax=axes[0], x='z', y='DailySnow', data=df_1951_1986, showfliers=False, color='skyblue')
axes[0].set_xlabel('Elevation (m)')
axes[0].set_ylabel('Snowdays per year')
axes[0].set_title('1951-1986')

# Rotate x-axis labels for better readability
axes[0].tick_params(axis='x', rotation=45)

# Subplot 2: 1986-2022
sns.boxplot(ax=axes[1], x='z', y='DailySnow', data=df_1986_2022, showfliers=False, color='lightcoral')
axes[1].set_xlabel('Elevation (m)')
axes[1].set_ylabel('Snowdays per year')
axes[1].set_title('1986-2022')

# Rotate x-axis labels for better readability
axes[1].tick_params(axis='x', rotation=45)

# Adjust layout for better appearance
plt.tight_layout()

# Show the plot
plt.show()

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ... (Your existing code for loading and processing data)

# Convert 'z' column to integers (if not already)
combined_df['z'] = combined_df['z'].astype(int)

# Create a new column to represent the time period
combined_df['Period'] = pd.cut(combined_df['Year'], bins=[1951, 1986, 2022], labels=['1951-1986', '1986-2022'])

# Create a boxplot for both time periods in one plot
plt.figure(figsize=(12, 8))

# Boxplot for both time periods
sns.boxplot(x='z', y='DailySnow', hue='Period', data=combined_df, showfliers=False, palette=['skyblue', 'lightcoral'])

# Set labels and title
plt.xlabel('Elevation (m)', fontsize=32)
plt.ylabel('Snowdays per year', fontsize=32)
#plt.title('Snow Days per Year Comparison (1951-1986 and 1986-2022)')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, fontsize=26)
plt.yticks(fontsize=26)
# Add a legend
plt.legend(title='Period')

# Show the plot
plt.show()

# Calculate average snow days per year for each elevation and period
average_snowdays_per_elevation_period = combined_df.groupby(['z', 'Period'])['DailySnow'].mean().reset_index()

# Pivot the DataFrame to have periods as columns
average_snowdays_pivot = average_snowdays_per_elevation_period.pivot(index='z', columns='Period', values='DailySnow')

# Calculate the average decrease in snow days per year
average_decrease = average_snowdays_pivot['1951-1986'] - average_snowdays_pivot['1986-2022']

# Print the results
print("Average Decrease in Snow Days per Year:")
print(average_decrease)

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ... (Your existing code for loading and processing data)

# Convert 'z' column to integers (if not already)
combined_df['z'] = combined_df['z'].astype(int)

# Create a new column to represent the time period
combined_df['Period'] = pd.cut(combined_df['Year'], bins=[1951, 1986, 2022], labels=['1951-1986', '1986-2022'])

# Create a boxplot for both time periods in one plot
plt.figure(figsize=(12, 8))

# Boxplot for both time periods
sns.boxplot(x='z', y='DailySnow', hue='Period', data=combined_df, showfliers=False, palette=['skyblue', 'lightcoral'])

# Set labels and title
plt.xlabel('Elevation (m)', fontsize=32)
plt.ylabel('Snowdays per year', fontsize=32)
#plt.title('Snow Days per Year Comparison (1951-1986 and 1986-2022)')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, fontsize=26)
plt.yticks(fontsize=26)

legend = plt.legend(title='Period', fontsize=26, loc='lower right')
legend.get_title().set_fontsize(26)
# Add a legend
#plt.legend(title='Period')
#plt.xticks(plt.xticks()[0][::3])

# Show the plot
plt.show()

# Calculate average snow days per year for each elevation and period
average_snowdays_per_elevation_period = combined_df.groupby(['z', 'Period'])['DailySnow'].mean().reset_index()

# Pivot the DataFrame to have periods as columns
average_snowdays_pivot = average_snowdays_per_elevation_period.pivot(index='z', columns='Period', values='DailySnow')

# Calculate the average decrease in snow days per year
average_decrease = average_snowdays_pivot['1951-1986'] - average_snowdays_pivot['1986-2022']

# Print the results
print("Average Decrease in Snow Days per Year:")
print(average_decrease)

# Plot the decrease in snow days against elevation
plt.figure(figsize=(12, 6))
plt.plot(average_decrease.index, average_decrease, marker='o', linestyle='-', color='green')
plt.xlabel('Elevation (m)', fontsize=16)
plt.ylabel('Average Decrease in Snow Days per Year', fontsize=16)
plt.title('Average Decrease in Snow Days per Year vs. Elevation', fontsize=18)
plt.grid(True)
plt.show()

# Calculate the overall average decrease across all elevations
overall_average_decrease = average_decrease.mean()

# Print the overall average decrease
print(f"Overall Average Decrease in Snow Days per Year: {overall_average_decrease:.2f}")
