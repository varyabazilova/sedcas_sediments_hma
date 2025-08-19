"""
Volume per Event Plotting for Debris Flow Data
Created for SedCas model output visualization

This script creates multi-panel scatter plots showing debris flow volume (dfs) 
vs debris flow potential (dfspot) organized by sediment limitation percentage 
and elevation bin.

Usage:
    python volume_per_event_plotting.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path
import glob

# =============================================================================
# CONFIGURATION - CHANGE THESE VARIABLES AS NEEDED
# =============================================================================
LOCATION = 'langtang'  # Change to 'mustang' if processing mustang data
METHOD = 'daily'       # Change to 'once' for once-yearly sediment input
LANDCOVER = 1          # Land cover to plot (1-5)
DATA_FOLDER = "/Users/varyabazilova/Desktop/paper2/202406_modelruns/processing_pipeline/test_data_for_claude/volume_per_event_data"

def load_landcover_data(landcover):
    """
    Load all percentage data for a specific landcover
    
    Args:
        landcover: Land cover number (1-5)
    
    Returns:
        pd.DataFrame: Combined data for all percentages
    """
    
    data_folder = Path(DATA_FOLDER)
    
    # Find all CSV files for this landcover
    pattern = f"{LOCATION}_{METHOD}_{landcover}landcover_*percent_volume_per_event_data.csv"
    files = list(data_folder.glob(pattern))
    
    if not files:
        print(f"No data files found for landcover {landcover}")
        print(f"Looking for pattern: {pattern}")
        print(f"In folder: {data_folder}")
        return pd.DataFrame()
    
    all_data = []
    
    for file in files:
        print(f"Loading: {file.name}")
        df = pd.read_csv(file)
        all_data.append(df)
    
    # Combine all data
    combined_data = pd.concat(all_data, ignore_index=True)
    print(f"Total events loaded: {len(combined_data)}")
    
    return combined_data

def create_percentage_elevation_plot(data, save_path=None):
    """
    Create scatter plot grid: percentage (x-axis) vs elevation_bin (y-axis)
    
    Args:
        data: DataFrame with debris flow events
        save_path: Optional path to save the plot
    
    Returns:
        matplotlib figure
    """
    
    if len(data) == 0:
        print("No data to plot!")
        return None
    
    # Get unique percentages and elevation bins
    percentages = sorted(data['percentage'].unique())
    
    # Define elevation bin order (highest to lowest for plotting)
    elevation_bin_order = [
        '>=6000', '5500-6000', '5000-5500', '4500-5000',
        '4000-4500', '3500-4000', '3000-3500', '2500-3000', '<2500'
    ]
    
    # Filter to only existing elevation bins in correct order
    available_bins = data['elevation_bin'].unique()
    elevation_bins = [bin_name for bin_name in elevation_bin_order if bin_name in available_bins]
    
    print(f"Percentages: {percentages}")
    print(f"Elevation bins: {elevation_bins}")
    
    # Create figure with subplots
    n_percentages = len(percentages)
    n_elevation_bins = len(elevation_bins)
    
    fig, axes = plt.subplots(n_elevation_bins, n_percentages, 
                            figsize=(n_percentages * 3, n_elevation_bins * 2.5),
                            sharey=False, sharex=False, facecolor='white')
    
    # Handle case of single row or column
    if n_elevation_bins == 1:
        axes = axes.reshape(1, -1)
    if n_percentages == 1:
        axes = axes.reshape(-1, 1)
    if n_elevation_bins == 1 and n_percentages == 1:
        axes = np.array([[axes]])
    
    # Color map for different months by season
    months = sorted(data['month'].unique())
    month_colors = {}
    
    # Define seasonal colors
    for month in months:
        if month in [1, 2, 3, 4, 10, 11, 12]:  # Pre-monsoon and Post-monsoon (Jan-Apr, Oct-Dec)
            if month in [1, 2, 3, 4]:
                month_colors[month] = 'grey'  # Pre-monsoon
            else:
                month_colors[month] = 'brown'  # Post-monsoon
        elif month in [5, 6, 7, 8, 9]:  # Monsoon (May-Sep)
            # Use viridis for monsoon months
            viridis_colors = plt.cm.viridis([0.0, 0.25, 0.5, 0.75, 1.0])
            monsoon_mapping = {5: viridis_colors[0], 6: viridis_colors[1], 7: viridis_colors[2], 
                             8: viridis_colors[3], 9: viridis_colors[4]}
            month_colors[month] = monsoon_mapping[month]
    
    # Create subplot for each percentage/elevation combination
    for i, elevation_bin in enumerate(elevation_bins):
        for j, percentage in enumerate(percentages):
            
            ax = axes[i, j]
            
            # Filter data for this combination
            subset = data[(data['elevation_bin'] == elevation_bin) & 
                         (data['percentage'] == percentage)]
            
            if len(subset) > 0:
                # Create scatter plot with different alphas for seasons
                for month in subset['month'].unique():
                    month_data = subset[subset['month'] == month]
                    
                    # Set alpha based on season
                    if month in [5, 6, 7, 8, 9]:  # Monsoon - full opacity
                        alpha = 1.0
                    else:  # Pre-monsoon and post-monsoon - reduced opacity
                        alpha = 0.7
                    
                    scatter = ax.scatter(
                        x=month_data['dfspot'], 
                        y=month_data['dfs'],
                        c=month_colors[month],
                        s=30,
                        alpha=alpha,
                        edgecolor='none'
                    )
                
                # Add 1:1 line
                max_val = max(subset['dfspot'].max(), subset['dfs'].max())
                if max_val > 0:
                    ax.plot([0, max_val], [0, max_val], 'r--', alpha=0.5, linewidth=1)
                
                # Set axis labels only on edges
                if i == n_elevation_bins - 1:  # Bottom row
                    ax.set_xlabel('DF Potential (mm)')
                if j == 0:  # Left column
                    ax.set_ylabel('DF Volume (mm)')
                
                # Add title for top row (percentage)
                if i == 0:
                    ax.set_title(f'{percentage}%')
                
                # Add elevation bin label on right side
                if j == n_percentages - 1:
                    ax.text(1.02, 0.5, elevation_bin, transform=ax.transAxes,
                           rotation=270, ha='left', va='center')
                
                # Add grid
                ax.grid(True, alpha=0.3)
                
                # Set white background for each subplot
                ax.set_facecolor('white')
                
                # Only show tick labels on leftmost and bottom panels
                if j != 0:  # Not leftmost column
                    ax.set_yticklabels([])
                if i != n_elevation_bins - 1:  # Not bottom row
                    ax.set_xticklabels([])
            
            else:
                # No data for this combination
                ax.text(0.5, 0.5, 'No events', transform=ax.transAxes,
                       ha='center', va='center', fontsize=8)
                ax.set_xlim(0, 1)
                ax.set_ylim(0, 1)
                
                # Set white background for empty panels
                ax.set_facecolor('white')
                
                # Set axis labels only on edges
                if i == n_elevation_bins - 1:
                    ax.set_xlabel('DF Potential (mm)')
                if j == 0:
                    ax.set_ylabel('DF Volume (mm)')
                
                # Add title for top row
                if i == 0:
                    ax.set_title(f'{percentage}%')
                
                # Add elevation bin label on right side
                if j == n_percentages - 1:
                    ax.text(1.02, 0.5, elevation_bin, transform=ax.transAxes,
                           rotation=270, ha='left', va='center')
                
                # Only show tick labels on leftmost and bottom panels
                if j != 0:  # Not leftmost column
                    ax.set_yticklabels([])
                if i != n_elevation_bins - 1:  # Not bottom row
                    ax.set_xticklabels([])
    
    # Add overall title
    fig.suptitle(f'DF Volume vs Potential - {LOCATION.title()} {METHOD.title()} LC{LANDCOVER}', 
                fontsize=16, y=0.98)
    
    # Add overall axis labels
    fig.text(0.5, 0.02, 'Sediment Limitation Percentage (%)', ha='center', fontsize=14)
    fig.text(0.02, 0.5, 'Elevation (m)', va='center', rotation='vertical', fontsize=14)
    
    # Adjust layout
    plt.tight_layout(rect=[0.03, 0.03, 0.97, 0.95])
    
    # Create legend with grouped seasons
    legend_elements = []
    
    # Add pre-monsoon (if exists)
    pre_monsoon_months = [m for m in months if m in [1, 2, 3, 4]]
    if pre_monsoon_months:
        legend_elements.append(plt.scatter([], [], c='grey', s=50, alpha=0.7, label='Pre-monsoon'))
    
    # Add individual monsoon months
    monsoon_months = [m for m in months if m in [5, 6, 7, 8, 9]]
    for month in sorted(monsoon_months):
        legend_elements.append(plt.scatter([], [], c=month_colors[month], s=50, label=f'Month {month}'))
    
    # Add post-monsoon (if exists)
    post_monsoon_months = [m for m in months if m in [10, 11, 12]]
    if post_monsoon_months:
        legend_elements.append(plt.scatter([], [], c='brown', s=50, alpha=0.7, label='Post-monsoon'))
    
    fig.legend(handles=legend_elements, title='Season/Month', loc='upper right', 
              bbox_to_anchor=(0.99, 0.99))
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    
    return fig

def main():
    """
    Main execution function
    """
    
    print(f"=== Volume per Event Plotting for {LOCATION.upper()} ({METHOD.upper()}) ===")
    print(f"Landcover: {LANDCOVER}")
    print(f"Data folder: {DATA_FOLDER}\n")
    
    # Load data for specified landcover
    data = load_landcover_data(LANDCOVER)
    
    if len(data) > 0:
        # Create plot
        output_file = f"{LOCATION}_{METHOD}_landcover{LANDCOVER}_percentage_elevation_scatter.png"
        output_path = Path("/Users/varyabazilova/Desktop/paper2/202406_modelruns/processing_pipeline/test_data_for_claude/dfs_vs_dfspot_plots") / output_file
        
        fig = create_percentage_elevation_plot(data, save_path=output_path)
        
        # Display summary statistics
        print(f"\n=== Data Summary ===")
        print(f"Total events: {len(data)}")
        print(f"Percentages: {sorted(data['percentage'].unique())}")
        print(f"Elevation bins: {sorted(data['elevation_bin'].unique())}")
        print(f"Date range: {data['D'].min()} to {data['D'].max()}")
        
        # Show events by percentage and elevation
        summary = data.groupby(['percentage', 'elevation_bin']).size().reset_index(name='event_count')
        print(f"\nEvents by percentage and elevation bin:")
        print(summary.pivot(index='elevation_bin', columns='percentage', values='event_count').fillna(0))
        
        if fig:
            plt.show()
    
    else:
        print("No data found! Check the data folder and file naming pattern.")

if __name__ == "__main__":
    main()