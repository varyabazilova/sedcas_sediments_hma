"""
Landcover and Method Comparison Plotting for Debris Flow Data
Created for SedCas model output visualization

This script creates multi-panel scatter plots comparing landcover 1 vs 5 
and daily vs once methods, with sediment limitation percentage on x-axis.

Usage:
    python landcover_method_comparison_plot.py
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
LANDCOVERS = [1, 5]    # Land covers to compare
METHODS = ['daily', 'once']  # Methods to compare
DATA_FOLDER = "/Users/varyabazilova/Desktop/paper2/202406_modelruns/processing_pipeline/test_data_for_claude/volume_per_event_data"

def load_landcover_method_data(landcover, method):
    """
    Load all percentage data for a specific landcover and method
    
    Args:
        landcover: Land cover number (1 or 5)
        method: Method ('daily' or 'once')
    
    Returns:
        pd.DataFrame: Combined data for all percentages
    """
    
    data_folder = Path(DATA_FOLDER)
    
    # Find all CSV files for this landcover and method
    pattern = f"{LOCATION}_{method}_{landcover}landcover_*percent_volume_per_event_data.csv"
    files = list(data_folder.glob(pattern))
    
    if not files:
        print(f"No data files found for landcover {landcover}, method {method}")
        print(f"Looking for pattern: {pattern}")
        return pd.DataFrame()
    
    all_data = []
    
    for file in files:
        print(f"Loading: {file.name}")
        df = pd.read_csv(file)
        all_data.append(df)
    
    # Combine all data
    if all_data:
        combined_data = pd.concat(all_data, ignore_index=True)
        print(f"  Events loaded: {len(combined_data)}")
        return combined_data
    else:
        return pd.DataFrame()

def create_landcover_method_comparison_plot(data_dict, save_path=None):
    """
    Create scatter plot grid: percentage (x-axis) vs landcover/method combinations (rows)
    
    Args:
        data_dict: Dictionary with keys like 'LC1_daily', 'LC1_once', etc.
        save_path: Optional path to save the plot
    
    Returns:
        matplotlib figure
    """
    
    # Check if we have data
    total_events = sum(len(df) for df in data_dict.values() if len(df) > 0)
    if total_events == 0:
        print("No data to plot!")
        return None
    
    # Get unique percentages from all data
    all_percentages = set()
    for df in data_dict.values():
        if len(df) > 0:
            all_percentages.update(df['percentage'].unique())
    percentages = sorted(list(all_percentages))
    
    print(f"Percentages found: {percentages}")
    
    # Define row structure: LC1-daily, LC1-once, LC5-daily, LC5-once
    row_configs = [
        ('LC1_daily', 'LC1 Daily'),
        ('LC1_once', 'LC1 Once'), 
        ('LC5_daily', 'LC5 Daily'),
        ('LC5_once', 'LC5 Once')
    ]
    
    # Create figure with subplots
    n_percentages = len(percentages)
    n_rows = len(row_configs)
    
    fig, axes = plt.subplots(n_rows, n_percentages, 
                            figsize=(n_percentages * 3, n_rows * 2.5),
                            sharey=False, sharex=False, facecolor='white')
    
    # Handle case of single row or column
    if n_rows == 1:
        axes = axes.reshape(1, -1)
    if n_percentages == 1:
        axes = axes.reshape(-1, 1)
    if n_rows == 1 and n_percentages == 1:
        axes = np.array([[axes]])
    
    # Define seasonal colors (same as before)
    def get_month_colors(months):
        month_colors = {}
        for month in months:
            if month in [1, 2, 3, 4, 10, 11, 12]:  # Pre-monsoon and Post-monsoon
                if month in [1, 2, 3, 4]:
                    month_colors[month] = 'grey'  # Pre-monsoon
                else:
                    month_colors[month] = 'brown'  # Post-monsoon
            elif month in [5, 6, 7, 8, 9]:  # Monsoon
                viridis_colors = plt.cm.viridis([0.0, 0.25, 0.5, 0.75, 1.0])
                monsoon_mapping = {5: viridis_colors[0], 6: viridis_colors[1], 7: viridis_colors[2], 
                                 8: viridis_colors[3], 9: viridis_colors[4]}
                month_colors[month] = monsoon_mapping[month]
        return month_colors
    
    # Create subplot for each row/percentage combination
    for i, (data_key, row_label) in enumerate(row_configs):
        for j, percentage in enumerate(percentages):
            
            ax = axes[i, j]
            
            # Get data for this combination
            if data_key in data_dict and len(data_dict[data_key]) > 0:
                data = data_dict[data_key]
                
                # Filter data for this percentage (lumping all elevations together)
                subset = data[data['percentage'] == percentage]
                
                if len(subset) > 0:
                    # Get month colors
                    months = subset['month'].unique()
                    month_colors = get_month_colors(months)
                    
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
                    if i == n_rows - 1:  # Bottom row
                        ax.set_xlabel('DF Potential (mm)')
                    if j == 0:  # Left column
                        ax.set_ylabel('DF Volume (mm)')
                    
                    # Add title for top row (percentage)
                    if i == 0:
                        ax.set_title(f'{percentage}%')
                    
                    # Add row label on right side
                    if j == n_percentages - 1:  # Rightmost column
                        ax.text(1.15, 0.5, row_label, transform=ax.transAxes,
                               rotation=270, ha='center', va='center', fontweight='bold')
                    
                    # Add grid
                    ax.grid(True, alpha=0.3)
                    
                    # Set white background for each subplot
                    ax.set_facecolor('white')
                    
                    # Add panel labels (A), (B), (C), etc.
                    panel_label = f"({chr(65 + i * n_percentages + j)})"  # (A), (B), (C), (D), ...
                    ax.text(0.05, 0.95, panel_label, transform=ax.transAxes,
                           fontsize=12, fontweight='bold', va='top', ha='left')
                    
                    # Only show tick labels on leftmost and bottom panels
                    if j != 0:  # Not leftmost column
                        ax.set_yticklabels([])
                    if i != n_rows - 1:  # Not bottom row
                        ax.set_xticklabels([])
                
                else:
                    # No data for this combination
                    ax.text(0.5, 0.5, 'No events', transform=ax.transAxes,
                           ha='center', va='center', fontsize=8)
                    ax.set_xlim(0, 1)
                    ax.set_ylim(0, 1)
                    
                    # Set white background
                    ax.set_facecolor('white')
                    
                    # Add panel labels (A), (B), (C), etc.
                    panel_label = f"({chr(65 + i * n_percentages + j)})"  # (A), (B), (C), (D), ...
                    ax.text(0.05, 0.95, panel_label, transform=ax.transAxes,
                           fontsize=12, fontweight='bold', va='top', ha='left')
                    
                    # Set axis labels and titles
                    if i == n_rows - 1:
                        ax.set_xlabel('DF Potential (mm)')
                    if j == 0:
                        ax.set_ylabel('DF Volume (mm)')
                    if i == 0:
                        ax.set_title(f'{percentage}%')
                    if j == n_percentages - 1:  # Rightmost column
                        ax.text(1.15, 0.5, row_label, transform=ax.transAxes,
                               rotation=270, ha='center', va='center', fontweight='bold')
                    
                    # Hide tick labels
                    if j != 0:
                        ax.set_yticklabels([])
                    if i != n_rows - 1:
                        ax.set_xticklabels([])
            
            else:
                # No data available for this landcover/method combination
                ax.text(0.5, 0.5, 'No data', transform=ax.transAxes,
                       ha='center', va='center', fontsize=8, color='red')
                ax.set_xlim(0, 1)
                ax.set_ylim(0, 1)
                ax.set_facecolor('white')
                
                # Add panel labels (A), (B), (C), etc.
                panel_label = f"({chr(65 + i * n_percentages + j)})"  # (A), (B), (C), (D), ...
                ax.text(0.05, 0.95, panel_label, transform=ax.transAxes,
                       fontsize=12, fontweight='bold', va='top', ha='left')
                
                # Set labels
                if i == n_rows - 1:
                    ax.set_xlabel('DF Potential (mm)')
                if j == 0:
                    ax.set_ylabel('DF Volume (mm)')
                if i == 0:
                    ax.set_title(f'{percentage}%')
                if j == n_percentages - 1:  # Rightmost column
                    ax.text(1.15, 0.5, row_label, transform=ax.transAxes,
                           rotation=270, ha='center', va='center', fontweight='bold')
                
                # Hide tick labels
                if j != 0:
                    ax.set_yticklabels([])
                if i != n_rows - 1:
                    ax.set_xticklabels([])
    
    # Add overall title
    fig.suptitle(f'DF Volume vs Potential - {LOCATION.title()} LC1 vs LC5 Comparison', 
                fontsize=16, y=0.98)
    
    # Add overall axis labels
    fig.text(0.5, 0.02, 'Sediment Limitation Percentage (%)', ha='center', fontsize=14)
    fig.text(0.02, 0.5, 'Landcover / Method', va='center', rotation='vertical', fontsize=14)
    
    # Adjust layout
    plt.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
    
    # Create legend with grouped seasons
    legend_elements = []
    
    # Add seasonal legend
    legend_elements.append(plt.scatter([], [], c='grey', s=50, alpha=0.7, label='Pre-monsoon'))
    
    # Add individual monsoon months (5-9)
    viridis_colors = plt.cm.viridis([0.0, 0.25, 0.5, 0.75, 1.0])
    monsoon_mapping = {5: viridis_colors[0], 6: viridis_colors[1], 7: viridis_colors[2], 
                     8: viridis_colors[3], 9: viridis_colors[4]}
    for month in [5, 6, 7, 8, 9]:
        legend_elements.append(plt.scatter([], [], c=monsoon_mapping[month], s=50, label=f'Month {month}'))
    
    legend_elements.append(plt.scatter([], [], c='brown', s=50, alpha=0.7, label='Post-monsoon'))
    
    fig.legend(handles=legend_elements, title='Season/Month', loc='upper center', 
              bbox_to_anchor=(0.5, -0.02), ncol=len(legend_elements))
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    
    return fig

def main():
    """
    Main execution function
    """
    
    print(f"=== Landcover and Method Comparison for {LOCATION.upper()} ===")
    print(f"Comparing LC1 vs LC5, Daily vs Once")
    print(f"Data folder: {DATA_FOLDER}\n")
    
    # Load data for all combinations
    data_dict = {}
    
    for landcover in LANDCOVERS:
        for method in METHODS:
            key = f"LC{landcover}_{method}"
            print(f"Loading data for {key}...")
            data = load_landcover_method_data(landcover, method)
            data_dict[key] = data
    
    # Check if we have any data
    total_events = sum(len(df) for df in data_dict.values())
    
    if total_events > 0:
        # Create plot
        output_file = f"{LOCATION}_landcover_method_comparison_scatter.png"
        output_path = Path("/Users/varyabazilova/Desktop/paper2/202406_modelruns/processing_pipeline/test_data_for_claude/dfs_vs_dfspot_plots") / output_file
        
        # Ensure output directory exists
        output_path.parent.mkdir(exist_ok=True)
        
        fig = create_landcover_method_comparison_plot(data_dict, save_path=output_path)
        
        # Display summary statistics
        print(f"\n=== Data Summary ===")
        for key, df in data_dict.items():
            if len(df) > 0:
                print(f"{key}: {len(df)} events, {len(df['percentage'].unique())} percentages")
            else:
                print(f"{key}: No data")
        
        if fig:
            plt.show()
    
    else:
        print("No data found! Check the data folder and file naming patterns.")

if __name__ == "__main__":
    main()