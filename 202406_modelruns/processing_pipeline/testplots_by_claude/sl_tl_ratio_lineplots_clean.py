"""
SL/TL Ratio Line Plot Visualization

This script creates a comprehensive visualization showing the ratio of Supply-Limited (SL) 
to Transport-Limited (TL) sediment yields across different landcover scenarios, 
percentile thresholds, elevations, and months using line plots.

Author: Generated with Claude Code
Date: 2025
"""

import functions
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# DEFINE SEDIMENT INPUT METHODS - Both daily and once will be processed

methods = ['daily', 'once']
location = 'mustang'



# ============================================================================
# FUNCTION DEFINITIONS
# ============================================================================

def prepare_for_plot(dfcount, column, landcover, new_name):
    """
    Prepare dataframe for plotting by melting and adding elevation bins.
    
    Parameters:
    -----------
    dfcount : pd.DataFrame
        Input dataframe with sediment data
    column : str
        Type of data ('count' or 'volume')
    landcover : str
        Landcover identifier
    new_name : str
        Name for the value column
    
    Returns:
    --------
    pd.DataFrame
        Processed dataframe ready for analysis
    """
    if column == 'count':
        melted = pd.melt(dfcount, id_vars=['D', 'D_year', 'D_month'], var_name='elevation', value_name=new_name)
        melted = melted.rename(columns={'D_year': 'year', 'D_month': 'month'})
    if column == 'volume':
        melted = pd.melt(dfcount, id_vars=['year', 'month'], var_name='elevation', value_name=new_name)
    
    # Process elevation data
    melted['elevation'] = melted['elevation'].astype(str).str.extract(r'^(\d+)')[0].astype(int)
    melted['elevation_bin'] = melted.apply(functions.bin_elevation500, axis=1)
    melted['date_id'] = melted['year'].astype(str) + "_" + melted['month'].astype(str) + "_" + melted['elevation'].astype(str)
    melted = melted.sort_values('date_id')
    melted['landcover'] = landcover
    
    return melted

def combine_percentiles_for_landcover(landcover_num, sl_data):
    """
    Combine all percentile data for a single landcover scenario.
    
    Parameters:
    -----------
    landcover_num : int
        Landcover number (1-5)
    sl_data : dict
        Dictionary containing SL data for all percentiles
    
    Returns:
    --------
    pd.DataFrame
        Combined dataframe with Q100 columns for all percentiles
    """
    base_key = f'SL_20percent_{landcover_num}landcover'
    combined_df = sl_data[base_key][['year', 'month', 'elevation', 'elevation_bin', 'date_id', 'landcover']].copy()
    
    # Add Q100 columns for all percentiles
    for pct in ['20percent', '30percent', '40percent', '50percent', '60percent']:
        key = f'SL_{pct}_{landcover_num}landcover'
        combined_df[f'Q100_{pct}'] = sl_data[key]['Q100'].values
    
    return combined_df

def add_tl_data_to_combined(combined_df, tl_df):
    """
    Add Transport-Limited (TL) data to the combined SL dataframe.
    
    Parameters:
    -----------
    combined_df : pd.DataFrame
        Combined SL dataframe
    tl_df : pd.DataFrame
        TL dataframe with Qstl values
    
    Returns:
    --------
    pd.DataFrame
        Merged dataframe with both SL and TL data
    """
    merged_df = combined_df.merge(
        tl_df[['year', 'month', 'elevation', 'elevation_bin', 'date_id', 'Qstl']],
        on=['year', 'month', 'elevation', 'elevation_bin', 'date_id'],
        how='left'
    )
    return merged_df

def calculate_sl_to_tl_percentages(df):
    """
    Calculate the percentage of SL (Q100) to TL (Qstl) for each percentile.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with both Q100 and Qstl columns
    
    Returns:
    --------
    pd.DataFrame
        Dataframe with added SL_to_TL percentage columns
    """
    df_with_percentages = df.copy()
    percentiles = ['20percent', '30percent', '40percent', '50percent', '60percent']
    
    for pct in percentiles:
        q100_col = f'Q100_{pct}'
        percentage_col = f'SL_to_TL_{pct}'
        
        # Calculate (Q100 / Qstl) * 100, handle division by zero
        df_with_percentages[percentage_col] = (
            df_with_percentages[q100_col] / df_with_percentages['Qstl'] * 100
        ).fillna(0)
        
        # Replace infinite values
        df_with_percentages[percentage_col] = df_with_percentages[percentage_col].replace(
            [float('inf'), -float('inf')], 0
        )
    
    return df_with_percentages

def plot_panel_lines(ax, data_daily, data_once, pct_col, percentage, show_yticks=False, show_xticks=False, show_legend=False):
    """
    Plot a single panel of the line chart grid with both daily and once data.
    
    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        Axes object to plot on
    data_daily : pd.DataFrame
        Daily method data for this panel
    data_once : pd.DataFrame
        Once method data for this panel
    pct_col : str
        Column name for the percentage data
    percentage : str
        Percentage value for y-axis label
    show_yticks : bool
        Whether to show y-axis labels
    show_xticks : bool
        Whether to show x-axis labels
    show_legend : bool
        Whether to show legend
    """
    # Plot lines for each elevation bin - both daily and once
    for j, elev_bin in enumerate(elevation_bins):
        # Daily data (solid lines)
        elev_data_daily = data_daily[data_daily['elevation_bin'] == elev_bin]
        monthly_means_daily = elev_data_daily.groupby('month')[pct_col].mean()
        months_list = sorted(data_daily['month'].unique())
        values_daily = [monthly_means_daily.get(month, 0) for month in months_list]
        
        ax.plot(months_list, values_daily, 
                color=colors[j], 
                linewidth=1.5,
                linestyle='-',  # Solid line for daily
                marker='o', 
                markersize=2,
                label=f'{elev_bin}m' if show_legend else "",
                alpha=0.8)
        
        # Once data (dashed lines)
        elev_data_once = data_once[data_once['elevation_bin'] == elev_bin]
        monthly_means_once = elev_data_once.groupby('month')[pct_col].mean()
        values_once = [monthly_means_once.get(month, 0) for month in months_list]
        
        ax.plot(months_list, values_once, 
                color=colors[j], 
                linewidth=1.5,
                linestyle='--',  # Dashed line for once
                marker='s', 
                markersize=2,
                alpha=0.8)
    
    # Add method indicators for legend (only on first panel)
    if show_legend:
        ax.plot([], [], 'k-', linewidth=1.5, label='Daily')
        ax.plot([], [], 'k--', linewidth=1.5, label='Once')
    
    # Add monsoon season highlighting
    ax.axvspan(5, 9, alpha=0.2, color='lightgrey', zorder=0)
    
    # Customize axes - smaller fonts for publication
    # Always set x-ticks for grid lines, but only show labels on bottom row
    ax.set_xticks(range(1, 13))
    if show_xticks:
        ax.set_xlabel('Month', fontsize=7)
        ax.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'], fontsize=6)
    else:
        ax.set_xticklabels([])
    
    # Set consistent y-ticks for all panels for grid lines
    ax.set_ylim(0, 100)
    ax.set_yticks(range(0, 101, 20))  # 0, 20, 40, 60, 80, 100
    if show_yticks:
        ax.set_ylabel(f'{percentage}%', fontsize=7)
        ax.tick_params(axis='y', labelsize=6)
    else:
        ax.set_yticklabels([])
    ax.grid(True, alpha=0.3, which='major', axis='both')

# ============================================================================
# DATA PROCESSING
# ============================================================================

# Load Transport-Limited (TL) data
print("Loading TL data...")
output_path = '/Users/varyabazilova/Desktop/paper2/202406_modelruns/30years/2025Jan_output/TL/'

TL_files = []
for i in range(1, 6):
    filename = f'{location}_monthly_sum_elevation_Qstl_{i}landcover_mm.csv'
    df = pd.read_csv(output_path + filename, index_col=0).fillna(0).reset_index().drop(['folder'], axis=1)
    TL_files.append(prepare_for_plot(df, 'volume', f'landcover {i}', 'Qstl'))

TL1, TL2, TL3, TL4, TL5 = TL_files

# Load Supply-Limited (SL) data for both methods
print("Loading SL data for both daily and once methods...")
percentiles = ['20percent', '30percent', '40percent', '50percent', '60percent']
landcovers = [1, 2, 3, 4, 5]
methods = ['daily', 'once']

sl_data_daily = {}
sl_data_once = {}

for method in methods:
    sl_base_path = f'/Users/varyabazilova/Desktop/paper2/202406_modelruns/30years/2025Jan_output/SL_{method}/'
    current_data = sl_data_daily if method == 'daily' else sl_data_once
    
    for pct in percentiles:
        for lc in landcovers:
            file_path = f'{sl_base_path}output_{pct}/{location}_monthly_sum_elevation_Q100_{pct}_{lc}landcover_mm.csv'
            key = f'SL_{pct}_{lc}landcover'
            df = pd.read_csv(file_path, index_col=0).fillna(0).reset_index().drop(['folder'], axis=1)
            current_data[key] = prepare_for_plot(df, 'volume', f'landcover {lc}', 'Q100')

# Combine percentiles for each landcover and method
print("Combining data for both methods...")
combined_landcovers_daily = {}
combined_landcovers_once = {}

for lc in [1, 2, 3, 4, 5]:
    combined_landcovers_daily[f'landcover_{lc}'] = combine_percentiles_for_landcover(lc, sl_data_daily)
    combined_landcovers_once[f'landcover_{lc}'] = combine_percentiles_for_landcover(lc, sl_data_once)

# Add TL data to combined datasets
tl_dataframes = [TL1, TL2, TL3, TL4, TL5]
for i, lc in enumerate([1, 2, 3, 4, 5]):
    combined_landcovers_daily[f'landcover_{lc}'] = add_tl_data_to_combined(
        combined_landcovers_daily[f'landcover_{lc}'],
        tl_dataframes[i]
    )
    combined_landcovers_once[f'landcover_{lc}'] = add_tl_data_to_combined(
        combined_landcovers_once[f'landcover_{lc}'],
        tl_dataframes[i]
    )

# Calculate SL/TL ratios for both methods
print("Calculating SL/TL ratios for both methods...")
for lc in [1, 2, 3, 4, 5]:
    combined_landcovers_daily[f'landcover_{lc}'] = calculate_sl_to_tl_percentages(combined_landcovers_daily[f'landcover_{lc}'])
    combined_landcovers_once[f'landcover_{lc}'] = calculate_sl_to_tl_percentages(combined_landcovers_once[f'landcover_{lc}'])

# Debug: Check if daily and once data are actually different
print("Debugging: Checking if daily vs once data are different...")
lc1_daily_sample = combined_landcovers_daily['landcover_1']['SL_to_TL_20percent'].head(10)
lc1_once_sample = combined_landcovers_once['landcover_1']['SL_to_TL_20percent'].head(10)
print(f"LC1 Daily 20% sample: {lc1_daily_sample.tolist()}")
print(f"LC1 Once 20% sample: {lc1_once_sample.tolist()}")
print(f"Are they identical? {lc1_daily_sample.equals(lc1_once_sample)}")

# ============================================================================
# VISUALIZATION
# ============================================================================

print("Creating visualization...")

# Get processed data for both methods
lc1_data_daily = combined_landcovers_daily['landcover_1']
lc2_data_daily = combined_landcovers_daily['landcover_2']
lc3_data_daily = combined_landcovers_daily['landcover_3']
lc4_data_daily = combined_landcovers_daily['landcover_4']
lc5_data_daily = combined_landcovers_daily['landcover_5']

lc1_data_once = combined_landcovers_once['landcover_1']
lc2_data_once = combined_landcovers_once['landcover_2']
lc3_data_once = combined_landcovers_once['landcover_3']
lc4_data_once = combined_landcovers_once['landcover_4']
lc5_data_once = combined_landcovers_once['landcover_5']

# Set up plotting parameters with consistent elevation-color mapping
# Define all possible elevation bins and assign fixed colors
all_elevation_bins = ['2500 - 3000', '3000 - 3500', '3500 - 4000', '4000 - 4500', 
                     '4500 - 5000', '5000 - 5500', '5500 - 6000', 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000]

# Create consistent color palette for all elevation bins - each bin gets unique color
elevation_color_map = {
    # Range elevation bins
    '2500 - 3000': '#1f77b4',  # Blue
    '3000 - 3500': '#ff7f0e',  # Orange  
    '3500 - 4000': '#2ca02c',  # Green
    '4000 - 4500': '#d62728',  # Red
    '4500 - 5000': '#9467bd',  # Purple
    '5000 - 5500': '#8c564b',  # Brown
    '5500 - 6000': '#e377c2',  # Pink
    # Single value elevation bins (different colors)
    2500: '#bcbd22',           # Olive
    3000: '#17becf',           # Cyan
    3500: '#aec7e8',           # Light blue
    4000: '#ffbb78',           # Light orange
    4500: '#98df8a',           # Light green
    5000: '#ff9896',           # Light red
    5500: '#c5b0d5',           # Light purple
    6000: '#f7b6d3',           # Light pink
    # String versions of single values
    '2500': '#bcbd22',         # Olive
    '3000': '#17becf',         # Cyan
    '3500': '#aec7e8',         # Light blue
    '4000': '#ffbb78',         # Light orange
    '4500': '#98df8a',         # Light green
    '5000': '#ff9896',         # Light red
    '5500': '#c5b0d5',         # Light purple
    '6000': '#f7b6d3'          # Light pink
}

# Get elevation bins present in current dataset
elevation_bins = sorted(lc1_data_daily['elevation_bin'].unique())
colors = [elevation_color_map[elev] for elev in elevation_bins]

# Create figure with mosaic layout - scaled for academic publication (half A4 page)
fig = plt.figure(figsize=(8.27, 5.5))  # Half A4 width (210mm = 8.27"), reasonable height
mosaic = """
        AaBbC
        DdEeF
        GgHhI
        JjKkL
        MmNnO
        """
axes = fig.subplot_mosaic(mosaic)

# Set column titles - smaller font for publication
axes['A'].set_title('Landcover 1', fontsize=8)
axes['a'].set_title('Landcover 2', fontsize=8)
axes['B'].set_title('Landcover 3', fontsize=8)
axes['b'].set_title('Landcover 4', fontsize=8)
axes['C'].set_title('Landcover 5', fontsize=8)

# Plot all panels using line plots with both daily and once data
# Row 1: 60%
plot_panel_lines(axes['A'], lc1_data_daily, lc1_data_once, 'SL_to_TL_60percent', '60', show_legend=True, show_yticks=True)
plot_panel_lines(axes['a'], lc2_data_daily, lc2_data_once, 'SL_to_TL_60percent', '60')
plot_panel_lines(axes['B'], lc3_data_daily, lc3_data_once, 'SL_to_TL_60percent', '60')
plot_panel_lines(axes['b'], lc4_data_daily, lc4_data_once, 'SL_to_TL_60percent', '60')
plot_panel_lines(axes['C'], lc5_data_daily, lc5_data_once, 'SL_to_TL_60percent', '60')

# Row 2: 50%
plot_panel_lines(axes['D'], lc1_data_daily, lc1_data_once, 'SL_to_TL_50percent', '50', show_yticks=True)
plot_panel_lines(axes['d'], lc2_data_daily, lc2_data_once, 'SL_to_TL_50percent', '50')
plot_panel_lines(axes['E'], lc3_data_daily, lc3_data_once, 'SL_to_TL_50percent', '50')
plot_panel_lines(axes['e'], lc4_data_daily, lc4_data_once, 'SL_to_TL_50percent', '50')
plot_panel_lines(axes['F'], lc5_data_daily, lc5_data_once, 'SL_to_TL_50percent', '50')

# Row 3: 40%
plot_panel_lines(axes['G'], lc1_data_daily, lc1_data_once, 'SL_to_TL_40percent', '40', show_yticks=True)
plot_panel_lines(axes['g'], lc2_data_daily, lc2_data_once, 'SL_to_TL_40percent', '40')
plot_panel_lines(axes['H'], lc3_data_daily, lc3_data_once, 'SL_to_TL_40percent', '40')
plot_panel_lines(axes['h'], lc4_data_daily, lc4_data_once, 'SL_to_TL_40percent', '40')
plot_panel_lines(axes['I'], lc5_data_daily, lc5_data_once, 'SL_to_TL_40percent', '40')

# Row 4: 30%
plot_panel_lines(axes['J'], lc1_data_daily, lc1_data_once, 'SL_to_TL_30percent', '30', show_yticks=True)
plot_panel_lines(axes['j'], lc2_data_daily, lc2_data_once, 'SL_to_TL_30percent', '30')
plot_panel_lines(axes['K'], lc3_data_daily, lc3_data_once, 'SL_to_TL_30percent', '30')
plot_panel_lines(axes['k'], lc4_data_daily, lc4_data_once, 'SL_to_TL_30percent', '30')
plot_panel_lines(axes['L'], lc5_data_daily, lc5_data_once, 'SL_to_TL_30percent', '30')

# Row 5: 20% (bottom row with x-axis labels)
plot_panel_lines(axes['M'], lc1_data_daily, lc1_data_once, 'SL_to_TL_20percent', '20', show_yticks=True, show_xticks=True)
plot_panel_lines(axes['m'], lc2_data_daily, lc2_data_once, 'SL_to_TL_20percent', '20', show_xticks=True)
plot_panel_lines(axes['N'], lc3_data_daily, lc3_data_once, 'SL_to_TL_20percent', '20', show_xticks=True)
plot_panel_lines(axes['n'], lc4_data_daily, lc4_data_once, 'SL_to_TL_20percent', '20', show_xticks=True)
plot_panel_lines(axes['O'], lc5_data_daily, lc5_data_once, 'SL_to_TL_20percent', '20', show_xticks=True)

# Add horizontal legend below all panels
handles, labels = axes['A'].get_legend_handles_labels()
fig.legend(handles, labels, title=None, 
           bbox_to_anchor=(0.5, 0.015), loc='lower center',
           fontsize=7, ncol=4, title_fontsize=8)

# Adjust layout for publication with bottom legend
plt.tight_layout()
plt.subplots_adjust(top=0.92, left=0.08, right=0.98, bottom=0.18, hspace=0.3, wspace=0.2)

# Save plot in publication-ready formats
outpath = '/Users/varyabazilova/Desktop/paper2/202406_modelruns/processing_pipeline/testplots_by_claude/'

# Save as high-resolution PNG for publication
plt.savefig(outpath + f'sl_tl_ratio_lineplots_daily_vs_once_publication_{location}.png', 
           dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')

# Save as PDF for vector graphics (preferred for publications)
plt.savefig(outpath + f'sl_tl_ratio_lineplots_daily_vs_once_publication_{location}.pdf', 
           bbox_inches='tight', facecolor='white', edgecolor='none')

print(f"Publication-ready plots saved to: {outpath}")
print(f"Files: sl_tl_ratio_lineplots_publication.png and sl_tl_ratio_lineplots_daily_vs_once_publication_{location}.pdf")

plt.show()