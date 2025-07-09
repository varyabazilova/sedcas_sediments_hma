#!/usr/bin/env python3
"""
Combined locations bar plots script
Creates a single plot with:
- Upper row: Langtang bar plots (5 panels) with Qstl volume as bars and dfspot count as line
- Lower row: Mustang bar plots (5 panels) with Qstl volume as bars and dfspot count as line
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

def create_combined_locations_plot(langtang_data, mustang_data):
    """Create combined plot with Langtang on top and Mustang on bottom"""
    
    # Prepare data for both locations
    langtang_qstl, langtang_count = langtang_data
    mustang_qstl, mustang_count = mustang_data
    
    # Only use original Qstl columns
    qstl_original_cols = ['Qstl1', 'Qstl2', 'Qstl3', 'Qstl4', 'Qstl5']
    
    # Prepare Langtang data
    langtang_qstl_data = langtang_qstl[['month', 'elevation_bin'] + qstl_original_cols]
    langtang_df = langtang_qstl_data.melt(id_vars=['month', 'elevation_bin'], 
                                         var_name='variable', value_name='value')
    langtang_count_df = langtang_count.melt(id_vars=['month', 'elevation_bin'], 
                                           var_name='variable', value_name='value')
    
    # Prepare Mustang data
    mustang_qstl_data = mustang_qstl[['month', 'elevation_bin'] + qstl_original_cols]
    mustang_df = mustang_qstl_data.melt(id_vars=['month', 'elevation_bin'], 
                                       var_name='variable', value_name='value')
    mustang_count_df = mustang_count.melt(id_vars=['month', 'elevation_bin'], 
                                         var_name='variable', value_name='value')
    
    # Get variables
    variables = langtang_df['variable'].unique()
    num_vars = len(variables)  # Should be 5
    
    print(f"Creating plot with {num_vars} variables: {variables}")
    
    # Create figure with 2-row layout
    fig = plt.figure(figsize=(4*num_vars, 10))
    gs = gridspec.GridSpec(2, num_vars, height_ratios=[1, 1], hspace=0.1, wspace=0.3)
    
    # Arrays to store axes
    langtang_axes = []
    langtang_sec_axes = []
    mustang_axes = []
    mustang_sec_axes = []
    
    # Create axes for both rows
    for i in range(num_vars):
        # Langtang (upper row)
        sharey_l = langtang_axes[0] if i > 0 else None
        ax_l = fig.add_subplot(gs[0, i], sharey=sharey_l)
        langtang_axes.append(ax_l)
        ax_l_sec = ax_l.twinx()
        langtang_sec_axes.append(ax_l_sec)
        
        # Mustang (lower row)
        sharey_m = mustang_axes[0] if i > 0 else None
        ax_m = fig.add_subplot(gs[1, i], sharey=sharey_m)
        mustang_axes.append(ax_m)
        ax_m_sec = ax_m.twinx()
        mustang_sec_axes.append(ax_m_sec)
    
    # Plot Langtang (upper row)
    for i, var in enumerate(variables):
        ax = langtang_axes[i]
        ax_sec = langtang_sec_axes[i]
        
        # Bar plot for Qstl volume
        df_var = langtang_df[langtang_df['variable'] == var]
        df_monthly = df_var.groupby('month')['value'].mean().reset_index()
        
        sns.barplot(
            data=df_monthly,
            x='month',
            y='value',
            color='steelblue',
            ax=ax
        )
        
        # Add grey background shading for monsoon months (May to September)
        ax.axvspan(4.5, 8.5, color='grey', alpha=0.1)
        
        # Labels and formatting
        ax.set_xlabel('')
        ax.tick_params(labelbottom=False)
        if i == 0:
            ax.set_ylabel('Mean Qstl [mm/month]', fontsize=12)
        else:
            ax.set_ylabel('')
            ax.tick_params(labelleft=False)
        
        # Panel labels
        panel_label = f'L{i+1}'
        ax.text(0.05, 0.95, panel_label, transform=ax.transAxes, 
                fontsize=14, fontweight='bold', va='top', ha='left')
        
        # Line plot for dfcount
        df_var_count = langtang_count_df[langtang_count_df['variable'] == var]
        df_monthly_count = df_var_count.groupby('month')['value'].mean().reset_index()
        
        ax_sec.plot(df_monthly_count['month'], df_monthly_count['value'], 
                   color='peru', marker='o', linestyle='-', linewidth=2)
        
        if i == num_vars - 1:
            ax_sec.set_ylabel('DF count/month', color='peru', fontsize=12)
            ax_sec.tick_params(axis='y', colors='peru', labelsize=12, labelright=True)
        else:
            ax_sec.set_ylabel('')
            ax_sec.tick_params(axis='y', labelleft=False, labelright=False)
    
    # Plot Mustang (lower row)
    for i, var in enumerate(variables):
        ax = mustang_axes[i]
        ax_sec = mustang_sec_axes[i]
        
        # Bar plot for Qstl volume
        df_var = mustang_df[mustang_df['variable'] == var]
        df_monthly = df_var.groupby('month')['value'].mean().reset_index()
        
        sns.barplot(
            data=df_monthly,
            x='month',
            y='value',
            color='steelblue',
            ax=ax
        )
        
        # Add grey background shading for monsoon months (May to September)
        ax.axvspan(4.5, 8.5, color='grey', alpha=0.1)
        
        # Labels and formatting
        ax.set_xlabel('Month', fontsize=12)
        if i == 0:
            ax.set_ylabel('Mean Qstl [mm/month]', fontsize=12)
        else:
            ax.set_ylabel('')
            ax.tick_params(labelleft=False)
        
        # Panel labels
        panel_label = f'M{i+1}'
        ax.text(0.05, 0.95, panel_label, transform=ax.transAxes, 
                fontsize=14, fontweight='bold', va='top', ha='left')
        
        # Line plot for dfcount
        df_var_count = mustang_count_df[mustang_count_df['variable'] == var]
        df_monthly_count = df_var_count.groupby('month')['value'].mean().reset_index()
        
        ax_sec.plot(df_monthly_count['month'], df_monthly_count['value'], 
                   color='peru', marker='o', linestyle='-', linewidth=2)
        
        if i == num_vars - 1:
            ax_sec.set_ylabel('DF count/month', color='peru', fontsize=12)
            ax_sec.tick_params(axis='y', colors='peru', labelsize=12, labelright=True)
        else:
            ax_sec.set_ylabel('')
            ax_sec.tick_params(axis='y', labelleft=False, labelright=False)
    
    # Sync y-axes within each location
    # Langtang primary y-axes
    l_ymins = [ax.get_ylim()[0] for ax in langtang_axes]
    l_ymaxs = [ax.get_ylim()[1] for ax in langtang_axes]
    l_global_ymin = min(l_ymins)
    l_global_ymax = max(l_ymaxs)
    for ax in langtang_axes:
        ax.set_ylim(l_global_ymin, l_global_ymax)
    
    # Langtang secondary y-axes
    l_sec_ymins = [ax.get_ylim()[0] for ax in langtang_sec_axes]
    l_sec_ymaxs = [ax.get_ylim()[1] for ax in langtang_sec_axes]
    l_sec_global_ymin = min(l_sec_ymins)
    l_sec_global_ymax = max(l_sec_ymaxs)
    for ax in langtang_sec_axes:
        ax.set_ylim(l_sec_global_ymin, l_sec_global_ymax)
    
    # Mustang primary y-axes
    m_ymins = [ax.get_ylim()[0] for ax in mustang_axes]
    m_ymaxs = [ax.get_ylim()[1] for ax in mustang_axes]
    m_global_ymin = min(m_ymins)
    m_global_ymax = max(m_ymaxs)
    for ax in mustang_axes:
        ax.set_ylim(m_global_ymin, m_global_ymax)
    
    # Mustang secondary y-axes
    m_sec_ymins = [ax.get_ylim()[0] for ax in mustang_sec_axes]
    m_sec_ymaxs = [ax.get_ylim()[1] for ax in mustang_sec_axes]
    m_sec_global_ymin = min(m_sec_ymins)
    m_sec_global_ymax = max(m_sec_ymaxs)
    for ax in mustang_sec_axes:
        ax.set_ylim(m_sec_global_ymin, m_sec_global_ymax)
    
    # Add horizontal dashed line on upper panels at lower panel's max Y value
    for ax in langtang_axes:
        ax.axhline(y=m_global_ymax, color='lighgray', linestyle='--', linewidth=1, alpha=0.7)
    
    # Add location labels
    fig.text(0.02, 0.75, 'Langtang', fontsize=16, fontweight='bold', rotation=90, va='center')
    fig.text(0.02, 0.25, 'Mustang', fontsize=16, fontweight='bold', rotation=90, va='center')
    
    plt.tight_layout()
    
    return fig

def main():
    """Main function to create combined locations plot"""
    print("Loading data for both locations...")
    
    # Load data for both locations
    langtang_data = load_and_process_data('langtang')
    mustang_data = load_and_process_data('mustang')
    
    # Prepare combined dataframes
    langtang_combined = prepare_combined_dataframes(langtang_data)
    mustang_combined = prepare_combined_dataframes(mustang_data)
    
    print("Creating combined locations plot...")
    
    # Create combined plot
    fig = create_combined_locations_plot(langtang_combined, mustang_combined)
    
    # Save plot
    output_path = '/Users/varyabazilova/Desktop/paper2/202406_modelruns/processing_pipeline/testplots_by_claude/combined_locations_barplots.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"Plot saved to: {output_path}")

if __name__ == "__main__":
    main()