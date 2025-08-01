import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



# SL Data Loading
columns =['year', 'month', 'elevation', 'elevation_bin', 'id','dfs_count_20percent', 'dfs_count_30percent', 'dfs_count_40percent', 'dfs_count_50percent', 'dfs_count_60percent', 'dfspot_count']

sl_path = '/Users/varyabazilova/Desktop/paper2/202406_modelruns/30years/2025May_output/df_vs_floods/'

# Langtang daily data
SL1_LT_daily = pd.read_csv(sl_path + 'langtang_df_vs_floods_daily_landcover1.csv', index_col = 0)[columns]
SL2_LT_daily = pd.read_csv(sl_path + 'langtang_df_vs_floods_daily_landcover2.csv', index_col = 0)[columns]
SL3_LT_daily = pd.read_csv(sl_path + 'langtang_df_vs_floods_daily_landcover3.csv', index_col = 0)[columns]
SL4_LT_daily = pd.read_csv(sl_path + 'langtang_df_vs_floods_daily_landcover4.csv', index_col = 0)[columns]
SL5_LT_daily = pd.read_csv(sl_path + 'langtang_df_vs_floods_daily_landcover5.csv', index_col = 0)[columns]

# Langtang once data
SL1_LT_once = pd.read_csv(sl_path + 'langtang_df_vs_floods_once_landcover1.csv', index_col = 0)[columns]
SL2_LT_once = pd.read_csv(sl_path + 'langtang_df_vs_floods_once_landcover2.csv', index_col = 0)[columns]
SL3_LT_once = pd.read_csv(sl_path + 'langtang_df_vs_floods_once_landcover3.csv', index_col = 0)[columns]
SL4_LT_once = pd.read_csv(sl_path + 'langtang_df_vs_floods_once_landcover4.csv', index_col = 0)[columns]
SL5_LT_once = pd.read_csv(sl_path + 'langtang_df_vs_floods_once_landcover5.csv', index_col = 0)[columns]

# Mustang daily data
SL1_MT_daily = pd.read_csv(sl_path + 'mustang_df_vs_floods_daily_landcover1.csv', index_col = 0)[columns]
SL2_MT_daily = pd.read_csv(sl_path + 'mustang_df_vs_floods_daily_landcover2.csv', index_col = 0)[columns]
SL3_MT_daily = pd.read_csv(sl_path + 'mustang_df_vs_floods_daily_landcover3.csv', index_col = 0)[columns]
SL4_MT_daily = pd.read_csv(sl_path + 'mustang_df_vs_floods_daily_landcover4.csv', index_col = 0)[columns]
SL5_MT_daily = pd.read_csv(sl_path + 'mustang_df_vs_floods_daily_landcover5.csv', index_col = 0)[columns]

# Mustang once data
SL1_MT_once = pd.read_csv(sl_path + 'mustang_df_vs_floods_once_landcover1.csv', index_col = 0)[columns]
SL2_MT_once = pd.read_csv(sl_path + 'mustang_df_vs_floods_once_landcover2.csv', index_col = 0)[columns]
SL3_MT_once = pd.read_csv(sl_path + 'mustang_df_vs_floods_once_landcover3.csv', index_col = 0)[columns]
SL4_MT_once = pd.read_csv(sl_path + 'mustang_df_vs_floods_once_landcover4.csv', index_col = 0)[columns]
SL5_MT_once = pd.read_csv(sl_path + 'mustang_df_vs_floods_once_landcover5.csv', index_col = 0)[columns]

# Monthly means - Langtang daily
SL1_LT_daily_mean = SL1_LT_daily.groupby(['elevation_bin', 'month']).mean().reset_index()
SL2_LT_daily_mean = SL2_LT_daily.groupby(['elevation_bin', 'month']).mean().reset_index()
SL3_LT_daily_mean = SL3_LT_daily.groupby(['elevation_bin', 'month']).mean().reset_index()
SL4_LT_daily_mean = SL4_LT_daily.groupby(['elevation_bin', 'month']).mean().reset_index()
SL5_LT_daily_mean = SL5_LT_daily.groupby(['elevation_bin', 'month']).mean().reset_index()

# Monthly means - Langtang once
SL1_LT_once_mean = SL1_LT_once.groupby(['elevation_bin', 'month']).mean().reset_index()
SL2_LT_once_mean = SL2_LT_once.groupby(['elevation_bin', 'month']).mean().reset_index()
SL3_LT_once_mean = SL3_LT_once.groupby(['elevation_bin', 'month']).mean().reset_index()
SL4_LT_once_mean = SL4_LT_once.groupby(['elevation_bin', 'month']).mean().reset_index()
SL5_LT_once_mean = SL5_LT_once.groupby(['elevation_bin', 'month']).mean().reset_index()

# Monthly means - Mustang daily
SL1_MT_daily_mean = SL1_MT_daily.groupby(['elevation_bin', 'month']).mean().reset_index()
SL2_MT_daily_mean = SL2_MT_daily.groupby(['elevation_bin', 'month']).mean().reset_index()
SL3_MT_daily_mean = SL3_MT_daily.groupby(['elevation_bin', 'month']).mean().reset_index()
SL4_MT_daily_mean = SL4_MT_daily.groupby(['elevation_bin', 'month']).mean().reset_index()
SL5_MT_daily_mean = SL5_MT_daily.groupby(['elevation_bin', 'month']).mean().reset_index()

# Monthly means - Mustang once
SL1_MT_once_mean = SL1_MT_once.groupby(['elevation_bin', 'month']).mean().reset_index()
SL2_MT_once_mean = SL2_MT_once.groupby(['elevation_bin', 'month']).mean().reset_index()
SL3_MT_once_mean = SL3_MT_once.groupby(['elevation_bin', 'month']).mean().reset_index()
SL4_MT_once_mean = SL4_MT_once.groupby(['elevation_bin', 'month']).mean().reset_index()
SL5_MT_once_mean = SL5_MT_once.groupby(['elevation_bin', 'month']).mean().reset_index()

def create_location_plot(location_name, daily_data, once_data, y_limit=None):
    """Create a 2x5 subplot for one location (daily top, once bottom)"""
    fig, axes = plt.subplots(2, 5, figsize=(20, 8), sharey=False)
    fig.suptitle(f'{location_name}: Debris Flow Count by Frequency and Landcover', fontsize=16, y=0.98)
    
    landcover_labels = ['Landcover 1', 'Landcover 2', 'Landcover 3', 'Landcover 4', 'Landcover 5']
    frequency_labels = ['Daily', 'Once']
    percentages = ['20percent', '30percent', '40percent', '50percent', '60percent']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    for row, (freq_data, freq_label) in enumerate(zip([daily_data, once_data], frequency_labels)):
        for col, (data, landcover_label) in enumerate(zip(freq_data, landcover_labels)):
            ax = axes[row, col]
            
            # Group by month only (average across elevation bins)
            monthly_means = data.groupby('month').mean()
            
            # Plot each percentage as a line
            for j, (pct, color) in enumerate(zip(percentages, colors)):
                col_name = f'dfs_count_{pct}'
                if col_name in monthly_means.columns:
                    ax.plot(monthly_means.index, monthly_means[col_name], 
                           color=color, marker='o', linewidth=2, markersize=4,
                           label=f'{pct.replace("percent", "%")}')
            
            # Plot dfspot_count as a dashed line
            if 'dfspot_count' in monthly_means.columns:
                ax.plot(monthly_means.index, monthly_means['dfspot_count'], 
                       color='black', marker='s', linewidth=2, markersize=4,
                       linestyle='--', label='DFspot', alpha=0.8)
            
            # Add light grey background for May-September (months 5-9)
            ax.axvspan(5, 9, alpha=0.2, color='lightgrey', zorder=0)
            
            # Customize subplot
            if row == 0:  # Top row - add landcover labels
                ax.set_title(landcover_label, fontsize=12)
            if col == 0:  # Left column - add frequency labels and y-axis
                ax.set_ylabel(f'{freq_label}\nMean Monthly DF Count', fontsize=10)
            if row == 1:  # Bottom row - add x-axis labels
                ax.set_xlabel('Month', fontsize=10)
            
            ax.set_xticks(range(1, 13))
            ax.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])
            ax.grid(True, alpha=0.3)
            
            # Add legend only to top-left subplot
            if row == 0 and col == 0:
                handles, labels = ax.get_legend_handles_labels()
                ax.legend(handles[::-1], labels[::-1], bbox_to_anchor=(0, 1), loc='upper left', fontsize=9)
            
            # Set y-axis limits if specified
            if y_limit is not None:
                ax.set_ylim(0, y_limit)
    
    plt.tight_layout()
    return fig

# Create plots for both locations
langtang_daily_data = [SL1_LT_daily_mean, SL2_LT_daily_mean, SL3_LT_daily_mean, SL4_LT_daily_mean, SL5_LT_daily_mean]
langtang_once_data = [SL1_LT_once_mean, SL2_LT_once_mean, SL3_LT_once_mean, SL4_LT_once_mean, SL5_LT_once_mean]
mustang_daily_data = [SL1_MT_daily_mean, SL2_MT_daily_mean, SL3_MT_daily_mean, SL4_MT_daily_mean, SL5_MT_daily_mean]
mustang_once_data = [SL1_MT_once_mean, SL2_MT_once_mean, SL3_MT_once_mean, SL4_MT_once_mean, SL5_MT_once_mean]


outpath = '/Users/varyabazilova/Desktop/paper2/202406_modelruns/processing_pipeline/testplots_by_claude/'

# Create Langtang plot
fig_langtang = create_location_plot('Langtang', langtang_daily_data, langtang_once_data)
fig_langtang.savefig(outpath + 'Langtang_SL_counts.png', dpi=300, bbox_inches='tight')

# Create Mustang plot with y-axis limit
fig_mustang = create_location_plot('Mustang', mustang_daily_data, mustang_once_data, y_limit=1.5)
fig_mustang.savefig(outpath + 'Mustang_SL_counts.png', dpi=300, bbox_inches='tight')

# plt.show()