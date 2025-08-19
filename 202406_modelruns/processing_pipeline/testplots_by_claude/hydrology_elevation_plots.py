"""
Hydrological Components by Elevation Plot

This script creates elevation plots showing hydrological components (AET, Q, glacier melt, 
snow melt, rainfall) across different elevations, months, and landcover scenarios.

Author: Generated with Claude Code
Date: 2025
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import numpy as np
import functions

# ============================================================================
# CONFIGURATION
# ============================================================================

# Set location - change this to 'langtang' or 'mustang'
location = 'mustang'

# Data paths
folder = '/Users/varyabazilova/Desktop/paper2/202406_modelruns/30years/output/1july_hydro/'

# ============================================================================
# FUNCTION DEFINITIONS
# ============================================================================

def prepare_for_plot(df, landcover, variable):
    """
    Prepare dataframe for plotting by melting and adding elevation bins.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe with hydrological data
    landcover : str
        Landcover identifier
    variable : str
        Variable name
    
    Returns:
    --------
    pd.DataFrame
        Processed dataframe ready for analysis
    """
    df = df.drop('folder', axis=1)
    melted = pd.melt(df, id_vars=['year', 'month'], var_name='elevation', value_name='value')
    
    melted['elevation'] = melted['elevation'].astype(str).str.extract(r'^(\d+)')[0].astype(int)
    melted['elevation_bin'] = melted.apply(functions.bin_elevation500, axis=1)
    melted['date_id'] = melted['year'].astype(str) + "_" + melted['month'].astype(str) + "_" + melted['elevation'].astype(str)
    melted = melted.sort_values('date_id')
    melted['landcover'] = landcover
    melted['variable'] = variable
    return melted

def adjust_data(df):
    """
    Adjust data by making certain variables negative (outflows).
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
        
    Returns:
    --------
    pd.DataFrame
        Adjusted dataframe with negative values for outflows
    """
    df = df.copy()  # Avoid modifying the original data
    df.loc[df["variable"].str.contains(r"\b(?:aet|Q|snowmelt)", regex=True, na=False), "value"] *= -1  
    return df

def group_data(data):
    """
    Group data by month, elevation_bin, and variable, calculating mean values.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Input dataframe
        
    Returns:
    --------
    pd.DataFrame
        Grouped dataframe with mean values
    """
    grouped = (
        data.groupby(['month', 'elevation_bin', 'variable'])['value']
        .mean()
        .reset_index()
    )
    return grouped

# ============================================================================
# DATA LOADING AND PROCESSING
# ============================================================================

print(f"Loading hydrological data for {location}...")

# Load data for all landcovers (1-5)
landcover_data = {}
base_names = ["aet", "Q", "glmelt", "snowmelt", "rainfall"]

for landcover_idx in range(1, 6):
    print(f"Processing landcover {landcover_idx}...")
    
    # Load data for each component
    aet = pd.read_csv(f'{folder}{location}/{location}_monthly_sum_elevation_AET_{landcover_idx}landcover_mm.csv')
    Q = pd.read_csv(f'{folder}{location}/{location}_monthly_sum_elevation_Q_{landcover_idx}landcover_mm.csv')
    glmelt = pd.read_csv(f'{folder}{location}/{location}_monthly_sum_elevation_glacier_melt_{landcover_idx}landcover_mm.csv')
    snowmelt = pd.read_csv(f'{folder}{location}/{location}_monthly_sum_elevation_snowmelt_{landcover_idx}landcover_mm.csv')
    rainfall = pd.read_csv(f'{folder}{location}/{location}_monthly_sum_elevation_rainfall_{landcover_idx}landcover_mm.csv')
    
    # Store in dictionary for easy access
    landcover_data[landcover_idx] = {
        'aet': aet,
        'Q': Q,
        'glmelt': glmelt,
        'snowmelt': snowmelt,
        'rainfall': rainfall
    }

# Process data for each landcover
print("Processing and preparing data...")
combined_dfs = []

for landcover_idx in range(1, 6):
    dataset_names = [f"{name}{landcover_idx}" for name in base_names]
    
    # Prepare each dataframe and add a column to differentiate them
    prepared_dfs = []
    for i, name in enumerate(dataset_names):
        component_name = base_names[i]  # Get the base name (without number)
        df = prepare_for_plot(
            landcover_data[landcover_idx][component_name], 
            f"landcover {landcover_idx}", 
            variable=name
        )
        df["type"] = name  # Add a new column with the dataset name
        prepared_dfs.append(df)
    
    # Concatenate all prepared dataframes for this landcover
    combined_df = pd.concat(prepared_dfs)
    
    # Adjust data (make outflows negative)
    combined_df = adjust_data(combined_df)
    
    combined_dfs.append(combined_df)

# Group data for plotting
print("Grouping data for plotting...")
grouped_dfs = []

for df in combined_dfs:
    grouped_df = group_data(df)
    # Remove numbers from variable names for cleaner plotting
    grouped_df['variable'] = grouped_df['variable'].str.replace(r'\d+$', '', regex=True)
    grouped_dfs.append(grouped_df)

# ============================================================================
# VISUALIZATION
# ============================================================================

print("Creating elevation plots...")

# Get unique variables, months, and elevation bins
variables = grouped_dfs[0]['variable'].unique()
months = sorted(grouped_dfs[0]['month'].unique())
elevation_bins = sorted(grouped_dfs[0]['elevation_bin'].unique())

# Define which months to highlight (monsoon season)
highlight_months = [5, 6, 7, 8, 9]
cmap = cm.get_cmap('viridis_r', len(highlight_months))

# Assign colors: vivid for monsoon months (5–9), light gray for others
colors = {}
for month in months:
    if month in highlight_months:
        idx = highlight_months.index(month)
        colors[month] = cmap(idx)
    else:
        colors[month] = (0.8, 0.8, 0.8, 0.9)  # light gray with transparency

# Prepare figure
num_vars = len(variables)
num_dfs = len(grouped_dfs)  # 5 landcovers
fig, axes = plt.subplots(num_dfs, num_vars, figsize=(20, 18), sharey=True, sharex=True)
fig.patch.set_facecolor('white')

# Fix axes shape for edge cases
if num_dfs == 1:
    axes = [axes]
if num_vars == 1:
    axes = [[ax] for ax in axes]

# Create the elevation plots
for row_idx, df in enumerate(grouped_dfs):
    for col_idx, var in enumerate(variables):
        ax = axes[col_idx][row_idx]
        df_var = df[df['variable'] == var]

        for month in months:
            df_month = df_var[df_var['month'] == month]
            # Thicker lines for monsoon months
            lw = 2.5 if month in highlight_months else 0.5

            ax.plot(
                df_month['value'],
                df_month['elevation_bin'],
                label=f'Month {month}',
                color=colors[month],
                linewidth=lw
            )

        # Add labels and titles
        if row_idx == 0:
            ax.set_ylabel(f'{var}', fontsize=14)
        if col_idx == 0:
            ax.set_title(f'Landcover {row_idx + 1}', fontsize=14)
        if row_idx == 0 and col_idx == 0:
            ax.legend(fontsize=10)

# Adjust layout
plt.tight_layout()

# Save plot
output_path = '/Users/varyabazilova/Desktop/paper2/202406_modelruns/processing_pipeline/testplots_by_claude/'
output_filename = f'{location}_hydrology_elevation.png'

plt.savefig(output_path + output_filename, bbox_inches='tight', dpi=300)
print(f"Plot saved as: {output_path + output_filename}")

plt.show()