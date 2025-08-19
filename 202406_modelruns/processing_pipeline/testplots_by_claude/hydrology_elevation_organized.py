"""
Organized Hydrological Components by Elevation Plot

This script creates elevation plots organized as:
- Row 1: Precipitation (input) and Snow melt (common output) + Legend
- Row 2: Glacier melt for 5 landcovers  
- Row 3: Discharge (Q) for 5 landcovers

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
if location == 'mustang':
    folder = '/Users/varyabazilova/Desktop/paper2/202406_modelruns/30years/output/1july_hydro/'
if location == 'langtang':
    folder = '/Users/varyabazilova/Desktop/paper2/202406_modelruns/30years/output/hydro/'


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
    # Only make AET and snowmelt negative, keep Q (discharge) positive
    # df.loc[df["variable"].str.contains(r"\b(?:aet|snowmelt)", regex=True, na=False), "value"] *= -1  
    # Only make AET and snowmelt negative, keep Q (discharge) positive
    df.loc[df["variable"].str.contains(r"\b(?:aet|snowmelt)", regex=True, na=False), "value"] *= -1  

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

print("Creating organized elevation plots...")

# Get unique variables, months, and elevation bins
variables = grouped_dfs[0]['variable'].unique()
months = sorted(grouped_dfs[0]['month'].unique())
elevation_bins = sorted(grouped_dfs[0]['elevation_bin'].unique())

# Create month name mapping
month_names = {
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
}

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

# Create figure scaled for half A4 page in scientific article
fig = plt.figure(figsize=(10.0, 5.5))  # Wider but shorter for better proportions
fig.patch.set_facecolor('white')

# Create subplot layout: 3 rows
# Row 1: 2 plots + legend space
# Row 2: 5 plots (glacier melt)
# Row 3: 5 plots (discharge)
gs = fig.add_gridspec(3, 7, height_ratios=[1, 1, 1], width_ratios=[1, 1, 1, 1, 1, 1, 1])

# Function to plot elevation data
def plot_elevation_data(ax, df, variable, title, show_ylabel=False, ylabel_text=None, show_yticklabels=True, show_xlabel=False):
    df_var = df[df['variable'] == variable]
    
    for month in months:
        df_month = df_var[df_var['month'] == month]
        # Thicker lines for monsoon months
        lw = 2.5 if month in highlight_months else 0.5
        
        ax.plot(
            df_month['value'],
            df_month['elevation_bin'],
            color=colors[month],
            linewidth=lw
        )
    
    if title:  # Only set title if provided
        ax.set_title(title, fontsize=10)
    ax.grid(True, alpha=0.3)
    
    if show_ylabel:
        ylabel = ylabel_text if ylabel_text else 'Elevation'
        ax.set_ylabel(ylabel, fontsize=10)
    
    if not show_yticklabels:
        ax.set_yticklabels([])
    
    if show_xlabel:
        ax.set_xlabel('[mm]', fontsize=9)
        ax.tick_params(axis='x', labelbottom=True, bottom=True)
    else:
        ax.set_xlabel('')
        ax.tick_params(axis='x', labelbottom=False, bottom=True)  # Keep ticks but hide labels
    
    # Set smaller tick label sizes for publication
    ax.tick_params(axis='both', labelsize=8)

# Store all axes for sharing x-axis
all_axes = []

# Row 1: Precipitation and Snow melt (use landcover 1 since they're the same)
df_lc1 = grouped_dfs[0]

# Precipitation panel
ax_precip = fig.add_subplot(gs[0, 0])
plot_elevation_data(ax_precip, df_lc1, 'rainfall', 'Precipitation', show_ylabel=True, ylabel_text='Elevation', show_yticklabels=True, show_xlabel=False)
all_axes.append(ax_precip)

# Snow melt panel  
ax_snow = fig.add_subplot(gs[0, 1])
plot_elevation_data(ax_snow, df_lc1, 'snowmelt', 'Snow Melt', show_ylabel=False, show_yticklabels=False, show_xlabel=False)
all_axes.append(ax_snow)

# Legend panel
ax_legend = fig.add_subplot(gs[0, 2:5])  # Move legend further left
ax_legend.axis('off')

# Create custom legend
legend_handles = []
legend_labels = []
for month in months:
    lw = 2.5 if month in highlight_months else 0.5
    line = plt.Line2D([0], [0], color=colors[month], linewidth=lw, label=month_names[month])
    legend_handles.append(line)
    legend_labels.append(month_names[month])

ax_legend.legend(legend_handles, legend_labels, loc='center left', fontsize=8, 
                title_fontsize=10, ncol=2)

# Row 2: Glacier melt for 5 landcovers
glacier_axes = []
for i in range(5):
    ax = fig.add_subplot(gs[1, i])
    df = grouped_dfs[i]
    show_ylabel = (i == 0)
    show_yticklabels = (i == 0)
    title = f'Landcover {i+1}'  # All landcover titles in row 2
    ylabel_text = 'Glacier Melt' if i == 0 else None
    plot_elevation_data(ax, df, 'glmelt', title, 
                       show_ylabel=show_ylabel, ylabel_text=ylabel_text, show_yticklabels=show_yticklabels, show_xlabel=False)
    glacier_axes.append(ax)
    all_axes.append(ax)

# Row 3: Discharge (Q) for 5 landcovers
discharge_axes = []
for i in range(5):
    ax = fig.add_subplot(gs[2, i])
    df = grouped_dfs[i]
    show_ylabel = (i == 0)
    show_yticklabels = (i == 0)
    show_xlabel = True  # Only bottom row gets x labels
    title = None  # No titles on bottom row
    ylabel_text = 'Discharge' if i == 0 else None
    plot_elevation_data(ax, df, 'Q', title, 
                       show_ylabel=show_ylabel, ylabel_text=ylabel_text, show_yticklabels=show_yticklabels, show_xlabel=show_xlabel)
    discharge_axes.append(ax)
    all_axes.append(ax)

# Remove the right-side variable labels since we're now using y-axis labels

# Don't share x-axis since we want different ticks for different variable types
# Set custom x-axis ticks based on variable type

# Set ticks for precipitation and snow melt (positive values: 0, 250, 500)
for ax in [ax_precip, ax_snow]:
    ax.set_xticks([0, 250, 500])

# Set ticks for glacier melt plots (positive values: 0, 250, 500)
for ax in glacier_axes:
    ax.set_xticks([0, 250, 500])

# Set ticks for discharge plots (negative values: -500, -250, 0)
for ax in discharge_axes:
    ax.set_xticks([0, 250, 500])

# Adjust layout
plt.tight_layout()

# Save plot in publication-ready formats
output_path = '/Users/varyabazilova/Desktop/paper2/202406_modelruns/processing_pipeline/testplots_by_claude/'
output_filename = f'{location}_hydrology_elevation_A4'

# Save as high-resolution PNG for publication
plt.savefig(output_path + output_filename + '.png', 
           dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')

# Save as PDF for vector graphics (preferred for publications)
plt.savefig(output_path + output_filename + '.pdf', 
           bbox_inches='tight', facecolor='white', edgecolor='none')

print(f"Publication-ready plots saved to: {output_path}")
print(f"Files: {output_filename}.png and {output_filename}.pdf")

plt.show()