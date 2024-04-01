# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 14:12:19 2023

@author: leon
"""

import os
import pandas as pd  # Import pandas
import matplotlib.pyplot as plt

# Directory containing CSV files
directory = r'D:\plotelevation\plotvegetation'

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        # Construct the full file path
        file_path = os.path.join(directory, filename)

        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Extract relevant columns
        x_values = df['Vegetation']
        y_values = df['Debriflow']
        z_values = df['z']
        
        plt.figure(figsize=(12, 8))
        
        # Create a scatter plot with a red to yellow colormap
        scatter = plt.scatter(x_values, y_values, c=z_values, cmap='plasma', marker='o',vmin=2500, vmax=5500, s=150)
        plt.tick_params(axis='both', labelsize=28)
        # Add colorbar
        cbar = plt.colorbar(scatter)
        cbar.set_label('Elevation (m)',  fontsize=30)
        cbar.ax.tick_params(labelsize=26)

        # Add labels and title
        plt.xlabel('Vegetation cover (%)', fontsize=32)
        plt.ylabel('Debris flow yield (mm)', fontsize=32)

        # Use the file name as the title
        #plt.title(f'{filename}')

        # Show the plot
        plt.show()
