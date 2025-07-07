#!/usr/bin/env python3
"""
Combined elevation plots script
Creates plots with:
- Upper panel: Barplots with Qstl volume as bars and dfspot count as line
- Lower panel: Heatmap showing change relative to landcover 1
- Columns correspond to landcovers 1-5 (landcover 1 lower panel is empty)
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import cm
import matplotlib.gridspec as gridspec
from functools import reduce
import sys
import os
sys.path.append('/Users/varyabazilova/Desktop/paper2/202406_modelruns/processing_pipeline')
import functions

def prepare_for_plot(dfcount, column, landcover, new_name):
    """Prepare data for plotting"""
    if column == 'count':
        melted = pd.melt(dfcount, id_vars=['D', 'D_year', 'D_month'], var_name='elevation', value_name=new_name) 
        melted = melted.rename(columns={'D_year': 'year', 'D_month': 'month'})
    if column == 'volume':
        melted = pd.melt(dfcount, id_vars=['year', 'month'], var_name='elevation', value_name=new_name)
    
    melted['elevation'] = melted['elevation'].astype(str).str.extract(r'^(\d+)')[0].astype(int)
    melted['elevation_bin'] = melted.apply(functions.bin_elevation500, axis=1)
    melted['date_id'] = melted['year'].astype(str) + "_" + melted['month'].astype(str) + "_" + melted['elevation'].astype(str)
    melted = melted.sort_values('date_id')
    melted['landcover'] = landcover
    return melted 

def count_mean_per_month(df):
    """Calculate mean count per month"""
    dfcount_mean = df.groupby('month')['dfcount'].mean().reset_index()
    dfcount_mean = dfcount_mean.rename(columns={'dfcount': 'dfcount_month_mean'})
    df = df.merge(dfcount_mean, on='month', how='left')
    return df

def group_data(data, landcover_idx, variable):
    """Group data by month and elevation bin"""
    grouped = (
        data.groupby(['month', 'elevation_bin'])[variable]
        .mean()
        .reset_index()
    )
    grouped = grouped.rename(columns={f'{variable}': f'Qstl{landcover_idx}'})
    return grouped

def load_and_process_data(location):
    """Load and process data for a given location"""
    print(f"Processing data for {location}...")
    
    # Define paths
    output_path = '/Users/varyabazilova/Desktop/paper2/202406_modelruns/30years/2025Jan_output/TL/'
    dfspot_path = '/Users/varyabazilova/Desktop/paper2/202406_modelruns/30years/2025May_output/dfspot/'
    
    # Load Qstl volume data
    TL_data = []
    for landcover_idx in range(1, 6):
        df = pd.read_csv(
            output_path + f'{location}_monthly_sum_elevation_Qstl_{landcover_idx}landcover_mm.csv', 
            index_col=0
        ).fillna(0).reset_index().drop(['folder'], axis=1)
        
        df_processed = prepare_for_plot(df, 'volume', f'landcover {landcover_idx}', 'Qstl')
        TL_data.append(df_processed)
    
    # Load dfspot count data
    TL_count_data = []
    for landcover_idx in range(1, 6):
        df_count = pd.read_csv(
            dfspot_path + f'{location}_monthly_dfspot_count_landcover{landcover_idx}.csv', 
            index_col=0
        ).fillna(0)
        
        df_count_processed = prepare_for_plot(df_count, 'count', f'landcover {landcover_idx}', 'dfcount')[['dfcount', 'date_id']]
        TL_count_data.append(df_count_processed)
    
    # Merge volume and count data
    for i in range(5):
        TL_data[i] = TL_data[i].merge(TL_count_data[i], on='date_id')
        TL_data[i] = count_mean_per_month(TL_data[i])
    
    return TL_data

def prepare_combined_dataframes(TL_data):
    """Prepare combined dataframes for plotting"""
    # Prepare Qstl volume data
    grouped_dfs_qstl = []
    for idx, df in enumerate(TL_data, start=1):
        grouped = group_data(df, landcover_idx=idx, variable='Qstl')
        grouped_dfs_qstl.append(grouped)
    
    combined_df_qstl = reduce(
        lambda left, right: pd.merge(left, right, on=['month', 'elevation_bin'], how='outer'),
        grouped_dfs_qstl
    )
    
    # Prepare dfcount data
    grouped_dfs_count = []
    for idx, df in enumerate(TL_data, start=1):
        grouped = group_data(df, landcover_idx=idx, variable='dfcount')
        grouped_dfs_count.append(grouped)
    
    combined_df_count = reduce(
        lambda left, right: pd.merge(left, right, on=['month', 'elevation_bin'], how='outer'),
        grouped_dfs_count
    )
    
    return combined_df_qstl, combined_df_count

def create_combined_plot(location, combined_df_qstl, combined_df_count, global_vmin=None, global_vmax=None):
    """Create the combined plot with upper and lower panels"""
    
    # Only use original Qstl columns for upper panels (not percentage columns)
    qstl_original_cols = ['Qstl1', 'Qstl2', 'Qstl3', 'Qstl4', 'Qstl5']
    qstl_data_only = combined_df_qstl[['month', 'elevation_bin'] + qstl_original_cols]
    
    # Prepare data for plotting
    mean_df = qstl_data_only.melt(id_vars=['month', 'elevation_bin'], 
                                 var_name='variable', 
                                 value_name='value')
    
    mean_df_count = combined_df_count.melt(id_vars=['month', 'elevation_bin'], 
                                          var_name='variable', 
                                          value_name='value')
    
    # Get unique variables and months
    variables = mean_df['variable'].unique()
    months = sorted(mean_df['month'].unique())
    num_vars = len(variables)  # Should be 5
    
    print(f"Debug: Found {num_vars} variables: {variables}")
    
    # Create figure with 2-panel layout - simpler approach
    fig = plt.figure(figsize=(4*num_vars + 1, 8))
    gs = gridspec.GridSpec(2, num_vars + 1, height_ratios=[1, 1], width_ratios=[1]*num_vars + [0.05], 
                          hspace=0.3, wspace=0.3)
    
    # Arrays to store axes
    bar_axes = []
    bar_sec_axes = []
    
    # Create upper panel axes (bar plots with line overlays)
    for i in range(num_vars):
        sharey_bar = bar_axes[0] if i > 0 else None
        ax_bar = fig.add_subplot(gs[0, i], sharey=sharey_bar)
        bar_axes.append(ax_bar)
        
        ax_bar_sec = ax_bar.twinx()
        bar_sec_axes.append(ax_bar_sec)
    
    # --- Upper panel: Bar plots with line overlays ---
    for i, var in enumerate(variables):
        ax = bar_axes[i]
        ax_sec = bar_sec_axes[i]
        
        # Bar plot for Qstl volume
        df_var = mean_df[mean_df['variable'] == var]
        df_monthly = df_var.groupby('month')['value'].mean().reset_index()
        
        sns.barplot(
            data=df_monthly,
            x='month',
            y='value',
            color='steelblue',
            ax=ax
        )
        
        ax.set_xlabel('Month', fontsize=12)
        if i == 0:
            ax.set_ylabel('Mean Qstl [mm/month]', fontsize=12)
        else:
            ax.set_ylabel('')
            ax.tick_params(labelleft=False)
        
        # Add grey background shading for months 5-9 (monsoon season)
        ax.axvspan(4.5, 9.5, color='grey', alpha=0.1)
        
        # Add panel labels in upper left corner
        location_prefix = location[0].upper()  # 'L' for langtang, 'M' for mustang
        panel_label = f'{location_prefix}{i+1}'
        ax.text(0.05, 0.95, panel_label, transform=ax.transAxes, 
                fontsize=14, fontweight='bold', va='top', ha='left')
        
        # Line plot for dfcount on secondary y-axis
        df_var_count = mean_df_count[mean_df_count['variable'] == var]
        df_monthly_count = df_var_count.groupby('month')['value'].mean().reset_index()
        
        ax_sec.plot(df_monthly_count['month'], df_monthly_count['value'], 
                   color='peru', marker='o', linestyle='-', linewidth=2)
        
        if i == num_vars - 1:
            ax_sec.set_ylabel('DF count/month', color='peru', fontsize=12)
            ax_sec.tick_params(axis='y', colors='peru', labelsize=12, labelright=True)
        else:
            ax_sec.set_ylabel('')
            ax_sec.tick_params(axis='y', labelleft=False, labelright=False)
    
    # Sync secondary y-axes
    sec_ymins = [ax.get_ylim()[0] for ax in bar_sec_axes]
    sec_ymaxs = [ax.get_ylim()[1] for ax in bar_sec_axes]
    global_ymin = min(sec_ymins)
    global_ymax = max(sec_ymaxs)
    
    for ax in bar_sec_axes:
        ax.set_ylim(global_ymin, global_ymax)
    
    # --- Lower panel: Heatmaps showing change relative to landcover 1 ---
    # Calculate percentages relative to Qstl1
    qstl_columns = ['Qstl2', 'Qstl3', 'Qstl4', 'Qstl5']
    for col in qstl_columns:
        combined_df_qstl[f'{col}_pct_of_Qstl1'] = (combined_df_qstl[col] / combined_df_qstl['Qstl1']) * 100
    
    grouped_pct = combined_df_qstl.groupby(['month', 'elevation_bin']).mean().reset_index()
    qstl_pct_cols = [f'{col}_pct_of_Qstl1' for col in qstl_columns]
    
    # Color range for heatmaps - use global values if provided
    if global_vmin is not None and global_vmax is not None:
        vmin = global_vmin
        vmax = global_vmax
    else:
        vmin = 0
        vmax = max(grouped_pct[qstl_pct_cols].max())
    
    quadmesh = None
    
    # First heatmap subplot: Empty (landcover 1 reference) - completely invisible
    ax_empty = fig.add_subplot(gs[1, 0])
    # Make everything invisible
    ax_empty.set_xticks([])
    ax_empty.set_yticks([])
    ax_empty.set_xlabel('')
    ax_empty.set_ylabel('')
    # Remove box around empty panel
    for spine in ax_empty.spines.values():
        spine.set_visible(False)
    ax_empty.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    
    # Heatmaps for landcovers 2-5
    for i, col in enumerate(qstl_pct_cols):
        ax = fig.add_subplot(gs[1, i + 1])  # Start from column 1
        data = grouped_pct.pivot(index='elevation_bin', columns='month', values=col)
        data = data.sort_index(ascending=False)
        
        hm = sns.heatmap(
            data,
            annot=True,
            cmap='coolwarm',
            center=100,
            ax=ax,
            cbar=False,  # No individual colorbars
            fmt='.0f',
            vmin=vmin,
            vmax=vmax,
            annot_kws={'size': 8}  # Smaller font size for annotations
        )
        
        if quadmesh is None:
            quadmesh = hm.collections[0]
        
        landcover_num = col.split('_')[0][-1]  # Extract number from 'Qstl2', etc.
        ax.set_xlabel('Month', fontsize=12)
        
        if i == 0:
            ax.set_ylabel('Elevation bin', fontsize=12)
        else:
            ax.set_ylabel('')
            ax.set_yticklabels([])
            ax.set_yticks([])
        
        # Add panel labels for heatmaps (continuing from upper panel numbering)
        location_prefix = location[0].upper()  # 'L' for langtang, 'M' for mustang
        panel_label = f'{location_prefix}{num_vars + i + 1}'  # Continue numbering from upper panels
        ax.text(0.05, 0.95, panel_label, transform=ax.transAxes, 
                fontsize=14, fontweight='bold', va='top', ha='left')
    
    # Add colorbar spanning only the second row (heatmap row) on the right side
    cbar_ax = fig.add_subplot(gs[1, -1])  # Only second row, last column
    cbar = fig.colorbar(quadmesh, cax=cbar_ax, label='% of Qstl1')
    cbar.set_label('% of Qstl1', fontsize=12)
    
    plt.tight_layout()
    
    return fig

def main():
    """Main function to create plots for both locations"""
    locations = ['langtang', 'mustang']
    
    # First pass: calculate global min/max for consistent colorbar
    global_min = float('inf')
    global_max = float('-inf')
    all_data = {}
    
    for location in locations:
        print(f"\nProcessing data for {location}...")
        
        # Load and process data
        TL_data = load_and_process_data(location)
        
        # Prepare combined dataframes
        combined_df_qstl, combined_df_count = prepare_combined_dataframes(TL_data)
        
        # Calculate percentages relative to Qstl1
        qstl_columns = ['Qstl2', 'Qstl3', 'Qstl4', 'Qstl5']
        for col in qstl_columns:
            combined_df_qstl[f'{col}_pct_of_Qstl1'] = (combined_df_qstl[col] / combined_df_qstl['Qstl1']) * 100
        
        grouped_pct = combined_df_qstl.groupby(['month', 'elevation_bin']).mean().reset_index()
        qstl_pct_cols = [f'{col}_pct_of_Qstl1' for col in qstl_columns]
        
        # Update global min/max
        current_min = grouped_pct[qstl_pct_cols].min().min()
        current_max = grouped_pct[qstl_pct_cols].max().max()
        global_min = min(global_min, current_min)
        global_max = max(global_max, current_max)
        
        # Store data for plotting
        all_data[location] = (TL_data, combined_df_qstl, combined_df_count)
    
    print(f"Global colorbar range: {global_min:.1f} to {global_max:.1f}")
    
    # Second pass: create plots with consistent colorbar
    for location in locations:
        print(f"\nCreating combined plot for {location}...")
        
        TL_data, combined_df_qstl, combined_df_count = all_data[location]
        
        # Create combined plot with global min/max
        fig = create_combined_plot(location, combined_df_qstl, combined_df_count, 
                                 global_vmin=global_min, global_vmax=global_max)
        
        # Save plot
        output_path = f'/Users/varyabazilova/Desktop/paper2/202406_modelruns/processing_pipeline/testplots_by_claude/{location}_combined_elevation_landcover_analysis.png'
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"Plot saved to: {output_path}")

if __name__ == "__main__":
    main()