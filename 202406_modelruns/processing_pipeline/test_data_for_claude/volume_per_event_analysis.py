"""
Volume per Event Analysis for Debris Flow Data
Created for SedCas model output processing

This script processes raw hourly model outputs to create scatter plots
showing debris flow volume (df) vs debris flow potential (dfspot) 
per elevation bin per month.

Usage:
    python volume_per_event_analysis.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path

# =============================================================================
# CONFIGURATION - CHANGE THESE VARIABLES AS NEEDED
# =============================================================================
LOCATION = 'mustang'  # Change to 'mustang' if processing mustang data
METHOD = 'once'  # Change to 'once' for once-yearly sediment input
ROOT_DATA_PATH = "/Volumes/T7 Shield/202409_paper2_modelruns/May2025_30years"  # Root path containing method folders
LANDCOVERS = [1, 2, 3, 4, 5]  # Land cover scenarios to process
PERCENTAGES = [20, 30, 40, 50, 60]  # Sediment limitation percentages to process

def bin_elevation500(row):
    """Function to create elevation bins (500m intervals)"""
    if row['elevation'] < 2500:
        return '<2500'
    elif 2500 <= row['elevation'] < 3000:
        return '2500-3000'
    elif 3000 <= row['elevation'] < 3500:
        return '3000-3500'
    elif 3500 <= row['elevation'] < 4000:
        return '3500-4000'
    elif 4000 <= row['elevation'] < 4500:
        return '4000-4500'
    elif 4500 <= row['elevation'] < 5000:
        return '4500-5000'
    elif 5000 <= row['elevation'] < 5500:
        return '5000-5500'
    elif 5500 <= row['elevation'] < 6000:
        return '5500-6000'
    elif 6000 <= row['elevation']:
        return '>=6000'

def process_volume_per_event_data(base_path, location=None):
    """
    Process raw hourly model outputs to create df vs dfspot table
    
    Args:
        base_path: path to folder containing elevation folders (e.g., 12a, 12b, etc.)
        location: 'langtang' or 'mustang' - determines which elevation file to use
                 If None, uses global LOCATION variable
    
    Returns:
        pd.DataFrame: Combined data with columns [D, dfs, dfspot, month, year, folder_name, elevation]
    """
    
    base_path = Path(base_path)
    all_data = []
    
    # Use global LOCATION if not specified
    if location is None:
        location = LOCATION
    
    # Load elevation data following existing workflow
    elevation_file = f'/Users/varyabazilova/Desktop/paper2/downscaling_simple/coordinates_and_elevation_with_labels_{location}.csv'
    
    if Path(elevation_file).exists():
        elevation = pd.read_csv(elevation_file)[['cellnr2', 'band_data']]
        elevation = elevation.transpose()
        elevation_list = elevation.loc['cellnr2'].tolist()
        elevation_mapping = dict(zip(elevation_list, elevation.loc['band_data']))
        print(f"Loaded elevation mapping for {location}: {len(elevation_mapping)} cells")
    else:
        # Fallback mapping
        elevation_mapping = {
            '12a': 4200, '12b': 4300, '12c': 4400, '12d': 4500, '13a': 4600
        }
        print(f"Using fallback elevation mapping: {len(elevation_mapping)} cells")
    
    print(f"Processing data from: {base_path}")
    
    # Iterate through all folder names (elevation cells)
    for folder in os.listdir(base_path):
        folder_path = base_path / folder
        
        if folder_path.is_dir() and folder in elevation_mapping:
            
            # Read raw sediment output
            sediment_file = folder_path / 'Sediment.out'
            
            if sediment_file.exists():
                print(f"Processing folder: {folder}")
                
                # Load hourly data
                df = pd.read_csv(sediment_file)
                df['D'] = pd.to_datetime(df['D'])
                
                # Filter only events where dfs > 0 (actual debris flows)
                events = df[df['dfs'] > 0].copy()
                
                if len(events) > 0:
                    # Add time components
                    events['month'] = events['D'].dt.month
                    events['year'] = events['D'].dt.year
                    
                    # Add folder name and elevation
                    events['folder_name'] = folder
                    events['elevation'] = elevation_mapping[folder]
                    
                    # Add elevation bin
                    events['elevation_bin'] = events.apply(bin_elevation500, axis=1)
                    
                    # Select relevant columns
                    events_clean = events[['D', 'dfs', 'dfspot', 'month', 'year', 'folder_name', 'elevation', 'elevation_bin']].copy()
                    
                    all_data.append(events_clean)
                    print(f"  Found {len(events)} debris flow events")
                else:
                    print(f"  No debris flow events found in {folder}")
            else:
                print(f"  Sediment.out not found in {folder}")
    
    if all_data:
        # Combine all data
        final_data = pd.concat(all_data, ignore_index=True)
        print(f"\nTotal events processed: {len(final_data)}")
        return final_data
    else:
        print("No data found!")
        return pd.DataFrame()

def create_df_dfspot_scatter(data, save_path=None):
    """
    Create scatter plot: df vs dfspot per elevation bin per month
    
    Args:
        data: DataFrame with debris flow events
        save_path: Optional path to save the plot
    
    Returns:
        matplotlib figure
    """
    
    if len(data) == 0:
        print("No data to plot!")
        return None
    
    # Group by month and elevation
    fig, axes = plt.subplots(3, 4, figsize=(20, 15))
    axes = axes.flatten()
    
    # Color map for elevations
    elevations = sorted(data['elevation'].unique())
    colors = plt.cm.viridis(np.linspace(0, 1, len(elevations)))
    elevation_colors = dict(zip(elevations, colors))
    
    for month in range(1, 13):
        ax = axes[month-1]
        month_data = data[data.month == month]
        
        if len(month_data) > 0:
            
            # Plot each elevation with different color
            for elevation in elevations:
                elev_data = month_data[month_data.elevation == elevation]
                if len(elev_data) > 0:
                    ax.scatter(
                        x=elev_data['dfspot'], 
                        y=elev_data['dfs'],
                        c=[elevation_colors[elevation]],
                        s=30,
                        alpha=0.7,
                        label=f'{elevation}m' if month == 1 else ""  # Legend only for first subplot
                    )
            
            ax.set_xlabel('DF Potential (mm)')
            ax.set_ylabel('DF Volume (mm)')
            ax.set_title(f'Month {month}')
            ax.grid(True, alpha=0.3)
            
            # Add 1:1 line
            if len(month_data) > 0:
                max_val = max(month_data['dfspot'].max(), month_data['dfs'].max())
                if max_val > 0:
                    ax.plot([0, max_val], [0, max_val], 'r--', alpha=0.5, linewidth=1)
        
        else:
            ax.text(0.5, 0.5, 'No events', transform=ax.transAxes, 
                   ha='center', va='center', fontsize=12)
            ax.set_xlabel('DF Potential (mm)')
            ax.set_ylabel('DF Volume (mm)')
            ax.set_title(f'Month {month}')
    
    # Add legend to first subplot
    if len(elevations) > 0:
        axes[0].legend(title='Elevation', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.suptitle('Debris Flow Volume vs Potential by Month and Elevation', fontsize=16)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    
    return fig

def create_summary_table(data):
    """
    Create summary statistics table
    
    Args:
        data: DataFrame with debris flow events
    
    Returns:
        pd.DataFrame: Summary statistics
    """
    
    if len(data) == 0:
        return pd.DataFrame()
    
    summary = data.groupby(['folder_name', 'elevation', 'elevation_bin', 'month']).agg({
        'dfs': ['count', 'mean', 'std', 'max'],
        'dfspot': ['mean', 'std', 'max']
    }).round(3)
    
    # Flatten column names
    summary.columns = [f"{col[1]}_{col[0]}" if col[1] != '' else col[0] 
                      for col in summary.columns]
    
    summary = summary.reset_index()
    
    return summary

def process_single_scenario(landcover, percentage):
    """
    Process a single landcover/percentage combination
    
    Args:
        landcover: Land cover number (1-5)
        percentage: Sediment limitation percentage (20-60)
    
    Returns:
        bool: True if successful, False if failed
    """
    
    # Construct path for this scenario
    scenario_folder = f"{landcover}landcover_{percentage}percent"
    base_path = Path(ROOT_DATA_PATH) / f"SL_{METHOD}" / scenario_folder / f"{LOCATION}_climate_cut"
    output_path = Path("/Users/varyabazilova/Desktop/paper2/202406_modelruns/processing_pipeline/test_data_for_claude")
    
    # Create output directory
    output_path.mkdir(exist_ok=True)
    
    print(f"\n--- Processing: {scenario_folder} ---")
    
    if not base_path.exists():
        print(f"  ERROR: Path does not exist: {base_path}")
        return False
    
    # Process data
    data = process_volume_per_event_data(base_path)
    
    if len(data) > 0:
        # Add scenario identifiers to the data
        data['landcover'] = f"landcover_{landcover}"
        data['percentage'] = f"{percentage}percent"
        data['method'] = METHOD
        data['scenario'] = scenario_folder
        
        # Create summary table
        summary = create_summary_table(data)
        summary_file = output_path / f"{LOCATION}_{METHOD}_{scenario_folder}_volume_per_event_summary.csv"
        summary.to_csv(summary_file, index=False)
        print(f"  Summary saved: {summary_file.name}")
        
        # Save processed data
        data_file = output_path / f"{LOCATION}_{METHOD}_{scenario_folder}_volume_per_event_data.csv" 
        data.to_csv(data_file, index=False)
        print(f"  Data saved: {data_file.name}")
        
        # Create scatter plot
        plot_file = output_path / f"{LOCATION}_{METHOD}_{scenario_folder}_df_vs_dfspot_scatter.png"
        fig = create_df_dfspot_scatter(data, save_path=plot_file)
        plt.close(fig)  # Close figure to save memory
        print(f"  Plot saved: {plot_file.name}")
        
        # Display basic statistics
        print(f"  Events found: {len(data)}")
        print(f"  Elevations: {len(data['elevation'].unique())} cells")
        
        return True
    
    else:
        print(f"  No debris flow events found for {scenario_folder}")
        return False

def main():
    """
    Main execution function - loops over all landcover/percentage combinations
    """
    
    print(f"=== Debris Flow Volume per Event Analysis for {LOCATION.upper()} ({METHOD.upper()}) ===")
    print(f"Root data path: {ROOT_DATA_PATH}/SL_{METHOD}")
    print(f"Processing {len(LANDCOVERS)} landcovers × {len(PERCENTAGES)} percentages = {len(LANDCOVERS) * len(PERCENTAGES)} scenarios\n")
    
    successful = 0
    failed = 0
    
    # Loop over all combinations
    for landcover in LANDCOVERS:
        for percentage in PERCENTAGES:
            try:
                success = process_single_scenario(landcover, percentage)
                if success:
                    successful += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"  ERROR processing landcover {landcover}, {percentage}%: {str(e)}")
                failed += 1
    
    print(f"\n=== Processing Complete ===")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total scenarios: {successful + failed}")

if __name__ == "__main__":
    main()