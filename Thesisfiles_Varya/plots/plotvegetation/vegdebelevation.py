# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 14:12:19 2023

@author: leon
"""

import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
file_path = r'D:\plotelevation\plotvegetation\langtang.csv'
df = pd.read_csv(file_path)

# Extract relevant columns
x_values = df['Vegetation']  # Vegetation on the y-axis
y_values = df['Debriflow']  # Debriflow in mm on the x-axis
z_values = df['Qss']  # Elevation for color representation

# Create a scatter plot with a red to yellow colormap
scatter = plt.scatter(x_values, y_values, c=z_values, cmap='Reds', marker='o')

# Add colorbar
cbar = plt.colorbar(scatter)
cbar.set_label('Elevation')

# Add labels and title
plt.xlabel('Vegetation')
plt.ylabel('Debriflow (mm)')
plt.title('Scatter Plot: Debriflow vs. Vegetation with Elevation Color Representation')

# Show the plot
plt.show()
