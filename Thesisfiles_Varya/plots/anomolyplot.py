import xarray as xr
import os
import matplotlib.pyplot as plt

# Specify the directory containing all the NetCDF files
directory_path = "D:\\climatedata\\era5land\\mustang\\temp"  # Replace with the actual directory path

# Get a list of all NetCDF files in the directory
file_paths = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.nc')]

# Open all NetCDF files and concatenate them along the time dimension
ds = xr.open_mfdataset(file_paths, combine='by_coords')

# Calculate the average temperature over all climate cells in Kelvin
average_temp_kelvin = ds['t2m'].mean(dim=['latitude', 'longitude'])

# Convert Kelvin to Celsius
average_temp_celsius = average_temp_kelvin - 273.15

# Calculate the baseline average temperature using all available data
baseline_avg = average_temp_celsius.mean(dim='time')

# Calculate temperature anomalies for all years
temperature_anomaly = average_temp_celsius - baseline_avg

# Calculate yearly average temperature anomaly
yearly_avg_anomaly = temperature_anomaly.groupby('time.year').mean(dim='time')

# Plot the yearly average temperature anomalies using a bar plot with color differentiation
colors = ['blue' if value < 0 else 'red' for value in yearly_avg_anomaly]
bars = plt.bar(yearly_avg_anomaly['year'], yearly_avg_anomaly, color=colors, alpha=0.7, label='Yearly Average Anomaly')

# Add a horizontal line at 0 to represent the baseline
plt.axhline(0, color='black', linestyle='--', label='Baseline')

# Customize the plot
plt.xlabel('Year')
plt.ylabel('Yearly Average Temperature Anomaly (°C)')
plt.ylim(-2.2, 2.2)
# Create custom legend entries
legend_entries = [plt.Line2D([0], [0], color='blue', lw=4, label='Cooler Years'),
                  plt.Line2D([0], [0], color='red', lw=4, label='Warmer Years'),
                  plt.Line2D([0], [0], color='black', linestyle='--', label='Baseline')]

# Add legend with custom entries
plt.legend(handles=legend_entries)

#plt.title('Yearly Average Temperature Anomaly Bar Plot')
plt.show()
