# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 14:12:19 2023

@author: leon
"""

import os
import pandas as pd  # Import pandas
import matplotlib.pyplot as plt

# Directory containing CSV files
directory = r"D:\Glacier_data\plotglaciertest"

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".out"):
        # Construct the full file path
        file_path = os.path.join(directory, filename)

        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Extract relevant columns
        x_values = df['glacier']
        y_values = df['Debri']
        z_values = df['melt']
        
        plt.figure(figsize=(12, 8))
        
        # Create a scatter plot with a red to yellow colormap
        scatter = plt.scatter(x_values, y_values, c=z_values, cmap='viridis', marker='o', s=150, vmin=500, vmax=4000)
        plt.tick_params(axis='both', labelsize=28)
        # Add colorbar
        cbar = plt.colorbar(scatter)
        cbar.set_label('Yearly average glacier melt (mm)',  fontsize=26)
        cbar.ax.tick_params(labelsize=26)

        # Add labels and title
        plt.xlabel('Glacier cover (%)', fontsize=32)
        plt.ylabel('Debris flow yield (mm)', fontsize=32)

        # Use the file name as the title
        #plt.title(f'{filename}')

        # Show the plot
        plt.show()
