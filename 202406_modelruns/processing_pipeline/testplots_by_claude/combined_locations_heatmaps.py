#!/usr/bin/env python3
"""
Combined locations heatmaps script
Creates a single plot with:
- Upper row: Langtang heatmaps (4 panels) showing landcovers 2-5 as % of landcover 1
- Lower row: Mustang heatmaps (4 panels) showing landcovers 2-5 as % of landcover 1
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import cmcrameri.cm as cmc
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
    
    return combined_df_qstl

def create_combined_heatmaps_plot(langtang_data, mustang_data, global_vmin, global_vmax):
    """Create combined heatmaps plot with Langtang on top and Mustang on bottom"""
    
    # Calculate percentages relative to Qstl1 for both locations
    qstl_columns = ['Qstl2', 'Qstl3', 'Qstl4', 'Qstl5']
    
    # Langtang percentages
    for col in qstl_columns:
        langtang_data[f'{col}_pct_of_Qstl1'] = (langtang_data[col] / langtang_data['Qstl1']) * 100
    
    # Mustang percentages
    for col in qstl_columns:
        mustang_data[f'{col}_pct_of_Qstl1'] = (mustang_data[col] / mustang_data['Qstl1']) * 100
    
    # Group data
    langtang_grouped = langtang_data.groupby(['month', 'elevation_bin']).mean().reset_index()
    mustang_grouped = mustang_data.groupby(['month', 'elevation_bin']).mean().reset_index()
    
    qstl_pct_cols = [f'{col}_pct_of_Qstl1' for col in qstl_columns]
    num_heatmaps = len(qstl_pct_cols)  # Should be 4
    
    print(f"Creating heatmaps plot with {num_heatmaps} heatmaps per location")
    
    # Create figure with 2-row layout + colorbar
    fig = plt.figure(figsize=(4*num_heatmaps + 1, 10))
    gs = gridspec.GridSpec(2, num_heatmaps + 1, height_ratios=[1, 1], 
                          width_ratios=[1]*num_heatmaps + [0.05], 
                          hspace=0.01, wspace=0.1)
    
    quadmesh = None
    


    # Plot Langtang heatmaps (upper row)
    for i, col in enumerate(qstl_pct_cols):
        ax = fig.add_subplot(gs[0, i])
        data = langtang_grouped.pivot(index='elevation_bin', columns='month', values=col)
        data = data.sort_index(ascending=False)
        
        hm = sns.heatmap(
            data,
            annot=True,
            # cmap=cmc.managua,
            cmap = 'RdBu_r',
            center=100,
            ax=ax,
            cbar=False,
            fmt='.0f',
            vmin=global_vmin,
            vmax=global_vmax,
            annot_kws={'size': 8}
        )
        
        if quadmesh is None:
            quadmesh = hm.collections[0]
        
        # Labels and formatting
        landcover_num = col.split('_')[0][-1]  # Extract number from 'Qstl2', etc.
        ax.set_xlabel('Month', fontsize=12)
        
        # Make monsoon months (5-9) bold
        xticklabels = ax.get_xticklabels()
        for j, label in enumerate(xticklabels):
            month_num = int(label.get_text()) if label.get_text().isdigit() else j+1
            if 5 <= month_num <= 9:
                label.set_fontweight('bold')
        
        if i == 0:
            ax.set_ylabel('Elevation bin', fontsize=12)
        else:
            ax.set_ylabel('')
            ax.set_yticklabels([])
            ax.set_yticks([])
        
        # Panel labels
        panel_label = f'L{i+2}'
        ax.text(0.05, 0.85, panel_label, transform=ax.transAxes, 
                fontsize=14, fontweight='bold', va='top', ha='left')
    
    # Plot Mustang heatmaps (lower row)
    for i, col in enumerate(qstl_pct_cols):
        ax = fig.add_subplot(gs[1, i])
        data = mustang_grouped.pivot(index='elevation_bin', columns='month', values=col)
        data = data.sort_index(ascending=False)
        
        hm = sns.heatmap(
            data,
            annot=True,
            # cmap=cmc.managua,
            cmap = 'RdBu_r',
            center=100,
            ax=ax,
            cbar=False,
            fmt='.0f',
            vmin=global_vmin,
            vmax=global_vmax,
            annot_kws={'size': 8}
        )
        
        # Labels and formatting
        landcover_num = col.split('_')[0][-1]  # Extract number from 'Qstl2', etc.
        ax.set_xlabel('Month', fontsize=12)
        
        # Make monsoon months (5-9) bold
        xticklabels = ax.get_xticklabels()
        for j, label in enumerate(xticklabels):
            month_num = int(label.get_text()) if label.get_text().isdigit() else j+1
            if 5 <= month_num <= 9:
                label.set_fontweight('bold')
        
        if i == 0:
            ax.set_ylabel('Elevation bin', fontsize=12)
        else:
            ax.set_ylabel('')
            ax.set_yticklabels([])
            ax.set_yticks([])
        
        # Panel labels
        panel_label = f'M{i+2}'
        ax.text(0.05, 0.85, panel_label, transform=ax.transAxes, 
                fontsize=14, fontweight='bold', va='top', ha='left')
    
    # Add colorbar spanning both rows
    cbar_ax = fig.add_subplot(gs[:, -1])  # Span both rows
    cbar = fig.colorbar(quadmesh, cax=cbar_ax, label='% of Qstl1')
    cbar.set_label('% of Qstl1', fontsize=12)
    
    # Add location labels
    fig.text(0.02, 0.75, 'Langtang', fontsize=16, fontweight='bold', rotation=90, va='center')
    fig.text(0.02, 0.25, 'Mustang', fontsize=16, fontweight='bold', rotation=90, va='center')
    
    plt.tight_layout()
    
    return fig

def main():
    """Main function to create combined heatmaps plot"""
    print("Loading data for both locations...")
    
    locations = ['langtang', 'mustang']
    all_data = {}
    
    # Load and process data for both locations
    for location in locations:
        TL_data = load_and_process_data(location)
        combined_df_qstl = prepare_combined_dataframes(TL_data)
        all_data[location] = combined_df_qstl
    
    # Calculate global min/max for consistent colorbar across both locations
    global_min = float('inf')
    global_max = float('-inf')
    
    qstl_columns = ['Qstl2', 'Qstl3', 'Qstl4', 'Qstl5']
    
    for location, combined_df_qstl in all_data.items():
        # Calculate percentages relative to Qstl1
        for col in qstl_columns:
            combined_df_qstl[f'{col}_pct_of_Qstl1'] = (combined_df_qstl[col] / combined_df_qstl['Qstl1']) * 100
        
        grouped_pct = combined_df_qstl.groupby(['month', 'elevation_bin']).mean().reset_index()
        qstl_pct_cols = [f'{col}_pct_of_Qstl1' for col in qstl_columns]
        
        # Update global min/max
        current_min = grouped_pct[qstl_pct_cols].min().min()
        current_max = grouped_pct[qstl_pct_cols].max().max()
        global_min = min(global_min, current_min)
        global_max = max(global_max, current_max)
    
    print(f"Global colorbar range: {global_min:.1f} to {global_max:.1f}")
    
    print("Creating combined heatmaps plot...")
    
    # Create combined plot with consistent colorbar
    fig = create_combined_heatmaps_plot(all_data['langtang'], all_data['mustang'], 
                                       global_min, global_max)
    
    # Save plot
    output_path = '/Users/varyabazilova/Desktop/paper2/202406_modelruns/processing_pipeline/testplots_by_claude/combined_locations_heatmaps.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"Plot saved to: {output_path}")

if __name__ == "__main__":
    main()