import pandas as pd
import matplotlib.pyplot as plt

# Load data
columns = ['year', 'month', 'elevation', 'elevation_bin', 'id','dfs_count_20percent', 'dfs_count_30percent', 'dfs_count_40percent', 'dfs_count_50percent', 'dfs_count_60percent', 'dfspot_count']
sl_path = '/Users/varyabazilova/Desktop/paper2/202406_modelruns/30years/2025May_output/df_vs_floods/'

# Load all landcover datasets
SL1_LT_daily = pd.read_csv(sl_path + 'langtang_df_vs_floods_daily_landcover1.csv', index_col=0)[columns]
SL2_LT_daily = pd.read_csv(sl_path + 'langtang_df_vs_floods_daily_landcover2.csv', index_col=0)[columns]
SL3_LT_daily = pd.read_csv(sl_path + 'langtang_df_vs_floods_daily_landcover3.csv', index_col=0)[columns]
SL4_LT_daily = pd.read_csv(sl_path + 'langtang_df_vs_floods_daily_landcover4.csv', index_col=0)[columns]
SL5_LT_daily = pd.read_csv(sl_path + 'langtang_df_vs_floods_daily_landcover5.csv', index_col=0)[columns]

# Group by elevation_bin and month for each landcover
SL1_mean_month = SL1_LT_daily.groupby(['elevation_bin', 'month']).mean().reset_index()
SL2_mean_month = SL2_LT_daily.groupby(['elevation_bin', 'month']).mean().reset_index()
SL3_mean_month = SL3_LT_daily.groupby(['elevation_bin', 'month']).mean().reset_index()
SL4_mean_month = SL4_LT_daily.groupby(['elevation_bin', 'month']).mean().reset_index()
SL5_mean_month = SL5_LT_daily.groupby(['elevation_bin', 'month']).mean().reset_index()

# Filter data for each elevation bin and landcover
# Landcover 1
SL1_elev_2500 = SL1_mean_month[SL1_mean_month['elevation_bin'] == 2500]
SL1_elev_3000 = SL1_mean_month[SL1_mean_month['elevation_bin'] == '2500 - 3000']
SL1_elev_3500 = SL1_mean_month[SL1_mean_month['elevation_bin'] == '3000 - 3500']
SL1_elev_4000 = SL1_mean_month[SL1_mean_month['elevation_bin'] == '3500 - 4000']
SL1_elev_4500 = SL1_mean_month[SL1_mean_month['elevation_bin'] == '4000 - 4500']
SL1_elev_5000 = SL1_mean_month[SL1_mean_month['elevation_bin'] == '4500 - 5000']
SL1_elev_5500 = SL1_mean_month[SL1_mean_month['elevation_bin'] == '5000 - 5500']
SL1_elev_6000 = SL1_mean_month[SL1_mean_month['elevation_bin'] == 6000]

# Landcover 2
SL2_elev_2500 = SL2_mean_month[SL2_mean_month['elevation_bin'] == 2500]
SL2_elev_3000 = SL2_mean_month[SL2_mean_month['elevation_bin'] == '2500 - 3000']
SL2_elev_3500 = SL2_mean_month[SL2_mean_month['elevation_bin'] == '3000 - 3500']
SL2_elev_4000 = SL2_mean_month[SL2_mean_month['elevation_bin'] == '3500 - 4000']
SL2_elev_4500 = SL2_mean_month[SL2_mean_month['elevation_bin'] == '4000 - 4500']
SL2_elev_5000 = SL2_mean_month[SL2_mean_month['elevation_bin'] == '4500 - 5000']
SL2_elev_5500 = SL2_mean_month[SL2_mean_month['elevation_bin'] == '5000 - 5500']
SL2_elev_6000 = SL2_mean_month[SL2_mean_month['elevation_bin'] == 6000]

# Landcover 3
SL3_elev_2500 = SL3_mean_month[SL3_mean_month['elevation_bin'] == 2500]
SL3_elev_3000 = SL3_mean_month[SL3_mean_month['elevation_bin'] == '2500 - 3000']
SL3_elev_3500 = SL3_mean_month[SL3_mean_month['elevation_bin'] == '3000 - 3500']
SL3_elev_4000 = SL3_mean_month[SL3_mean_month['elevation_bin'] == '3500 - 4000']
SL3_elev_4500 = SL3_mean_month[SL3_mean_month['elevation_bin'] == '4000 - 4500']
SL3_elev_5000 = SL3_mean_month[SL3_mean_month['elevation_bin'] == '4500 - 5000']
SL3_elev_5500 = SL3_mean_month[SL3_mean_month['elevation_bin'] == '5000 - 5500']
SL3_elev_6000 = SL3_mean_month[SL3_mean_month['elevation_bin'] == 6000]

# Landcover 4
SL4_elev_2500 = SL4_mean_month[SL4_mean_month['elevation_bin'] == 2500]
SL4_elev_3000 = SL4_mean_month[SL4_mean_month['elevation_bin'] == '2500 - 3000']
SL4_elev_3500 = SL4_mean_month[SL4_mean_month['elevation_bin'] == '3000 - 3500']
SL4_elev_4000 = SL4_mean_month[SL4_mean_month['elevation_bin'] == '3500 - 4000']
SL4_elev_4500 = SL4_mean_month[SL4_mean_month['elevation_bin'] == '4000 - 4500']
SL4_elev_5000 = SL4_mean_month[SL4_mean_month['elevation_bin'] == '4500 - 5000']
SL4_elev_5500 = SL4_mean_month[SL4_mean_month['elevation_bin'] == '5000 - 5500']
SL4_elev_6000 = SL4_mean_month[SL4_mean_month['elevation_bin'] == 6000]

# Landcover 5
SL5_elev_2500 = SL5_mean_month[SL5_mean_month['elevation_bin'] == 2500]
SL5_elev_3000 = SL5_mean_month[SL5_mean_month['elevation_bin'] == '2500 - 3000']
SL5_elev_3500 = SL5_mean_month[SL5_mean_month['elevation_bin'] == '3000 - 3500']
SL5_elev_4000 = SL5_mean_month[SL5_mean_month['elevation_bin'] == '3500 - 4000']
SL5_elev_4500 = SL5_mean_month[SL5_mean_month['elevation_bin'] == '4000 - 4500']
SL5_elev_5000 = SL5_mean_month[SL5_mean_month['elevation_bin'] == '4500 - 5000']
SL5_elev_5500 = SL5_mean_month[SL5_mean_month['elevation_bin'] == '5000 - 5500']
SL5_elev_6000 = SL5_mean_month[SL5_mean_month['elevation_bin'] == 6000]

# Create figure with 8x5 subplots (8 elevations x 5 landcovers)
fig, axes = plt.subplots(8, 5, figsize=(25, 16), sharex=True, sharey=True)
fig.suptitle('Langtang Daily: Debris Flow Count by Elevation and Landcover', fontsize=16, y=0.98)

# Colors
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

def plot_elevation_data(ax, elev_data, elev_label, is_leftmost=False, is_topmost=False, is_bottom=False):
    """Helper function to plot elevation data on a subplot"""
    ax.plot(elev_data['month'], elev_data['dfs_count_20percent'], color=colors[0], marker='o', linewidth=2, markersize=3, label='20%' if is_topmost else '')
    ax.plot(elev_data['month'], elev_data['dfs_count_30percent'], color=colors[1], marker='o', linewidth=2, markersize=3, label='30%' if is_topmost else '')
    ax.plot(elev_data['month'], elev_data['dfs_count_40percent'], color=colors[2], marker='o', linewidth=2, markersize=3, label='40%' if is_topmost else '')
    ax.plot(elev_data['month'], elev_data['dfs_count_50percent'], color=colors[3], marker='o', linewidth=2, markersize=3, label='50%' if is_topmost else '')
    ax.plot(elev_data['month'], elev_data['dfs_count_60percent'], color=colors[4], marker='o', linewidth=2, markersize=3, label='60%' if is_topmost else '')
    ax.plot(elev_data['month'], elev_data['dfspot_count'], color='black', marker='s', linewidth=2, markersize=3, linestyle='--', label='DFspot' if is_topmost else '', alpha=0.8)
    ax.axvspan(5, 9, alpha=0.2, color='lightgrey', zorder=0)
    
    if is_leftmost:
        ax.set_ylabel(f'{elev_label}m', fontsize=9)
    
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='both', labelsize=8)
    
    if is_bottom:
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])

# Column titles
landcover_titles = ['Landcover 1', 'Landcover 2', 'Landcover 3', 'Landcover 4', 'Landcover 5']
for col, title in enumerate(landcover_titles):
    axes[0, col].set_title(title, fontsize=12)

# Row 0: 6000m elevation
plot_elevation_data(axes[0, 0], SL1_elev_6000, '6000', is_leftmost=True, is_topmost=True)
plot_elevation_data(axes[0, 1], SL2_elev_6000, '6000', is_topmost=True)
plot_elevation_data(axes[0, 2], SL3_elev_6000, '6000', is_topmost=True)
plot_elevation_data(axes[0, 3], SL4_elev_6000, '6000', is_topmost=True)
plot_elevation_data(axes[0, 4], SL5_elev_6000, '6000', is_topmost=True)

# Row 1: 5500m elevation
plot_elevation_data(axes[1, 0], SL1_elev_5500, '5500', is_leftmost=True)
plot_elevation_data(axes[1, 1], SL2_elev_5500, '5500')
plot_elevation_data(axes[1, 2], SL3_elev_5500, '5500')
plot_elevation_data(axes[1, 3], SL4_elev_5500, '5500')
plot_elevation_data(axes[1, 4], SL5_elev_5500, '5500')

# Row 2: 5000m elevation
plot_elevation_data(axes[2, 0], SL1_elev_5000, '5000', is_leftmost=True)
plot_elevation_data(axes[2, 1], SL2_elev_5000, '5000')
plot_elevation_data(axes[2, 2], SL3_elev_5000, '5000')
plot_elevation_data(axes[2, 3], SL4_elev_5000, '5000')
plot_elevation_data(axes[2, 4], SL5_elev_5000, '5000')

# Row 3: 4500m elevation
plot_elevation_data(axes[3, 0], SL1_elev_4500, '4500', is_leftmost=True)
plot_elevation_data(axes[3, 1], SL2_elev_4500, '4500')
plot_elevation_data(axes[3, 2], SL3_elev_4500, '4500')
plot_elevation_data(axes[3, 3], SL4_elev_4500, '4500')
plot_elevation_data(axes[3, 4], SL5_elev_4500, '4500')

# Row 4: 4000m elevation
plot_elevation_data(axes[4, 0], SL1_elev_4000, '4000', is_leftmost=True)
plot_elevation_data(axes[4, 1], SL2_elev_4000, '4000')
plot_elevation_data(axes[4, 2], SL3_elev_4000, '4000')
plot_elevation_data(axes[4, 3], SL4_elev_4000, '4000')
plot_elevation_data(axes[4, 4], SL5_elev_4000, '4000')

# Row 5: 3500m elevation
plot_elevation_data(axes[5, 0], SL1_elev_3500, '3500', is_leftmost=True)
plot_elevation_data(axes[5, 1], SL2_elev_3500, '3500')
plot_elevation_data(axes[5, 2], SL3_elev_3500, '3500')
plot_elevation_data(axes[5, 3], SL4_elev_3500, '3500')
plot_elevation_data(axes[5, 4], SL5_elev_3500, '3500')

# Row 6: 3000m elevation
plot_elevation_data(axes[6, 0], SL1_elev_3000, '3000', is_leftmost=True)
plot_elevation_data(axes[6, 1], SL2_elev_3000, '3000')
plot_elevation_data(axes[6, 2], SL3_elev_3000, '3000')
plot_elevation_data(axes[6, 3], SL4_elev_3000, '3000')
plot_elevation_data(axes[6, 4], SL5_elev_3000, '3000')

# Row 7: 2500m elevation (bottom)
plot_elevation_data(axes[7, 0], SL1_elev_2500, '2500', is_leftmost=True, is_bottom=True)
plot_elevation_data(axes[7, 1], SL2_elev_2500, '2500', is_bottom=True)
plot_elevation_data(axes[7, 2], SL3_elev_2500, '2500', is_bottom=True)
plot_elevation_data(axes[7, 3], SL4_elev_2500, '2500', is_bottom=True)
plot_elevation_data(axes[7, 4], SL5_elev_2500, '2500', is_bottom=True)

# Add legend to top-left subplot
handles, labels = axes[0, 0].get_legend_handles_labels()
axes[0, 0].legend(handles[::-1], labels[::-1], bbox_to_anchor=(0, 1), loc='upper left', fontsize=8)

# Set common x and y labels
fig.text(0.5, 0.02, 'Month', ha='center', fontsize=12)

plt.tight_layout()

# Save plot
outpath = '/Users/varyabazilova/Desktop/paper2/202406_modelruns/processing_pipeline/testplots_by_claude/'
plt.savefig(outpath + 'elevation_lines_all_landcovers_langtang_daily.png', dpi=300, bbox_inches='tight')
plt.show()