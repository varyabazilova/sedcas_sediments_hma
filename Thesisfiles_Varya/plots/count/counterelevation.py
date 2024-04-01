# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 15:39:20 2023

@author: leon
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# Directory containing CSV files
directory = r'D:\plotelevation\count'

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        # Construct the full file path
        file_path = os.path.join(directory, filename)

        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Extract relevant columns
        x_values = df['Qdf']
        y_values = df['count']
        z_values = df['z']
        
        plt.figure(figsize=(12, 8))
        
        # Create a scatter plot with a red to yellow colormap
        scatter = plt.scatter(x_values, y_values, c=z_values, cmap='plasma', marker='o', vmin=2500, vmax=5500, s=150)
        plt.tick_params(axis='both', labelsize=28)
        # Add colorbar
        cbar = plt.colorbar(scatter)
        cbar.set_label('Elevation (m)', fontsize=30)
        cbar.ax.tick_params(labelsize=26)

        # Add labels and title
        plt.xlabel('Qdf (mm)', fontsize=32)
        plt.ylabel('Debris flow count', fontsize=32)

        # Use the file name as the title
        # plt.title(f'{filename}')

        # Show the plot
        plt.show()

        # Create a scatter plot with a red to yellow colormap and logarithmic scale on the y-axis
        plt.figure(figsize=(12, 8))
        scatter_log = plt.scatter(x_values, y_values + 1*10**-1, c=z_values, cmap='plasma', marker='o', vmin=2500, vmax=5500, s=150)
        plt.tick_params(axis='both', labelsize=28)
        # Add colorbar
        cbar_log = plt.colorbar(scatter_log)
        cbar_log.set_label('Elevation (m)', fontsize=30)
        cbar_log.ax.tick_params(labelsize=26)

        # Add labels and title
        plt.xlabel('Qdf (mm)', fontsize=32)
        plt.ylabel('Debris flow count', fontsize=32)

        # Use the file name as the title
        # plt.title(f'{filename}')

        # Make the y-axis logarithmic
        plt.yscale('log')

        # Show the plot
        plt.show()
