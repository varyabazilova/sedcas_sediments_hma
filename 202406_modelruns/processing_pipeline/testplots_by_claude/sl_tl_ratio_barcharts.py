import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Get landcover 1 and 2 data
lc1_data = combined_landcovers['landcover_1']
lc2_data = combined_landcovers['landcover_2']

# Set up the mosaic layout for 10 panels (5 for each landcover)
fig = plt.figure(figsize=(20, 12))
mosaic = """
        Aa
        Bb
        Cc
        Dd
        Ee
        """
axes = fig.subplot_mosaic(mosaic)

# Color palette for elevation bins
elevation_bins = sorted(lc1_data['elevation_bin'].unique())
colors = sns.color_palette("viridis", len(elevation_bins))

# Prepare common data
months = sorted(lc1_data['month'].unique())
x_pos = np.arange(len(months))
bar_width = 0.15

def plot_panel(ax, data, pct_col, title, show_legend=False):
    # Plot bars for each elevation bin
    for j, elev_bin in enumerate(elevation_bins):
        elev_data = data[data['elevation_bin'] == elev_bin]
        monthly_means = elev_data.groupby('month')[pct_col].mean()
        
        # Align data with months (fill missing with 0)
        values = [monthly_means.get(month, 0) for month in months]
        
        # Position bars
        x_positions = x_pos + (j - len(elevation_bins)/2 + 0.5) * bar_width
        
        ax.bar(x_positions, values, bar_width, 
               label=f'{elev_bin}m' if show_legend else "", 
               color=colors[j], alpha=0.8)
    
    # Customize subplot
    ax.set_title(title, fontsize=12)
    ax.set_xlabel('Month', fontsize=10)
    ax.set_ylabel('SL/TL Percentage', fontsize=10)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])
    ax.grid(True, alpha=0.3)
    
    if show_legend:
        ax.legend(title='Elevation', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)

# Landcover 1 panels (A, B, C, D, E)
plot_panel(axes['A'], lc1_data, 'SL_to_TL_60percent', 'Landcover 1 - 60%', show_legend=True)
plot_panel(axes['B'], lc1_data, 'SL_to_TL_50percent', 'Landcover 1 - 50%')
plot_panel(axes['C'], lc1_data, 'SL_to_TL_40percent', 'Landcover 1 - 40%')
plot_panel(axes['D'], lc1_data, 'SL_to_TL_30percent', 'Landcover 1 - 30%')
plot_panel(axes['E'], lc1_data, 'SL_to_TL_20percent', 'Landcover 1 - 20%')

# Landcover 2 panels (a, b, c, d, e)
plot_panel(axes['a'], lc2_data, 'SL_to_TL_60percent', 'Landcover 2 - 60%')
plot_panel(axes['b'], lc2_data, 'SL_to_TL_50percent', 'Landcover 2 - 50%')
plot_panel(axes['c'], lc2_data, 'SL_to_TL_40percent', 'Landcover 2 - 40%')
plot_panel(axes['d'], lc2_data, 'SL_to_TL_30percent', 'Landcover 2 - 30%')
plot_panel(axes['e'], lc2_data, 'SL_to_TL_20percent', 'Landcover 2 - 20%')

plt.suptitle('SL/TL Ratio Comparison: Landcover 1 vs Landcover 2', fontsize=16, y=0.95)
plt.tight_layout()

# Save plot
outpath = '/Users/varyabazilova/Desktop/paper2/202406_modelruns/processing_pipeline/testplots_by_claude/'
plt.savefig(outpath + 'sl_tl_ratio_barcharts_landcover1.png', dpi=300, bbox_inches='tight')
plt.show()