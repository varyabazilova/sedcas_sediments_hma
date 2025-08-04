import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Get all landcover data
lc1_data = combined_landcovers['landcover_1']
lc2_data = combined_landcovers['landcover_2']
lc3_data = combined_landcovers['landcover_3']
lc4_data = combined_landcovers['landcover_4']
lc5_data = combined_landcovers['landcover_5']

# Set up the mosaic layout for 25 panels (5 landcovers x 5 percentiles)
fig = plt.figure(figsize=(25, 12))
mosaic = """
        AaBbC
        DdEeF
        GgHhI
        JjKkL
        MmNnO
        """
axes = fig.subplot_mosaic(mosaic)

def plot_panel(ax, data, pct_col, title, show_legend=False, show_yticks=False, show_xticks=False):
    # Prepare data for heatmap
    pivot_data = data.pivot_table(
        values=pct_col, 
        index='elevation_bin', 
        columns='month', 
        aggfunc='mean'
    ).fillna(0)
    
    # Sort elevation bins from high to low (6000 at top, 2500 at bottom)
    pivot_data = pivot_data.sort_index(ascending=False)
    
    # Create y-tick labels handling both numeric and string elevation bins
    if show_yticks:
        ytick_labels = []
        for elev in pivot_data.index:
            if isinstance(elev, str):
                ytick_labels.append(f'{elev}m')
            else:
                ytick_labels.append(f'{int(elev)}m')
    else:
        ytick_labels = False
    
    # Create x-tick labels
    xtick_labels = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'] if show_xticks else False
    
    # Create heatmap
    sns.heatmap(pivot_data, 
                ax=ax,
                cmap='RdYlGn',  # Red = low SL/TL (high limitation), Green = high SL/TL (low limitation)
                cbar=show_legend,  # Only show colorbar on first panel
                annot=False,  # Set to True if you want values displayed
                fmt='.0f',
                xticklabels=xtick_labels,
                yticklabels=ytick_labels)
    
    # Customize subplot
    ax.set_title(title, fontsize=12)
    if show_xticks:
        ax.set_xlabel('Month', fontsize=10)
    if show_yticks:
        ax.set_ylabel('Elevation', fontsize=10)

# Row 1: 60% - All landcovers
plot_panel(axes['A'], lc1_data, 'SL_to_TL_60percent', 'LC1 - 60%', show_legend=True, show_yticks=True)
plot_panel(axes['a'], lc2_data, 'SL_to_TL_60percent', 'LC2 - 60%')
plot_panel(axes['B'], lc3_data, 'SL_to_TL_60percent', 'LC3 - 60%')
plot_panel(axes['b'], lc4_data, 'SL_to_TL_60percent', 'LC4 - 60%')
plot_panel(axes['C'], lc5_data, 'SL_to_TL_60percent', 'LC5 - 60%')

# Row 2: 50% - All landcovers
plot_panel(axes['D'], lc1_data, 'SL_to_TL_50percent', 'LC1 - 50%', show_yticks=True)
plot_panel(axes['d'], lc2_data, 'SL_to_TL_50percent', 'LC2 - 50%')
plot_panel(axes['E'], lc3_data, 'SL_to_TL_50percent', 'LC3 - 50%')
plot_panel(axes['e'], lc4_data, 'SL_to_TL_50percent', 'LC4 - 50%')
plot_panel(axes['F'], lc5_data, 'SL_to_TL_50percent', 'LC5 - 50%')

# Row 3: 40% - All landcovers
plot_panel(axes['G'], lc1_data, 'SL_to_TL_40percent', 'LC1 - 40%', show_yticks=True)
plot_panel(axes['g'], lc2_data, 'SL_to_TL_40percent', 'LC2 - 40%')
plot_panel(axes['H'], lc3_data, 'SL_to_TL_40percent', 'LC3 - 40%')
plot_panel(axes['h'], lc4_data, 'SL_to_TL_40percent', 'LC4 - 40%')
plot_panel(axes['I'], lc5_data, 'SL_to_TL_40percent', 'LC5 - 40%')

# Row 4: 30% - All landcovers
plot_panel(axes['J'], lc1_data, 'SL_to_TL_30percent', 'LC1 - 30%', show_yticks=True)
plot_panel(axes['j'], lc2_data, 'SL_to_TL_30percent', 'LC2 - 30%')
plot_panel(axes['K'], lc3_data, 'SL_to_TL_30percent', 'LC3 - 30%')
plot_panel(axes['k'], lc4_data, 'SL_to_TL_30percent', 'LC4 - 30%')
plot_panel(axes['L'], lc5_data, 'SL_to_TL_30percent', 'LC5 - 30%')

# Row 5: 20% - All landcovers (bottom row shows x-ticks)
plot_panel(axes['M'], lc1_data, 'SL_to_TL_20percent', 'LC1 - 20%', show_yticks=True, show_xticks=True)
plot_panel(axes['m'], lc2_data, 'SL_to_TL_20percent', 'LC2 - 20%', show_xticks=True)
plot_panel(axes['N'], lc3_data, 'SL_to_TL_20percent', 'LC3 - 20%', show_xticks=True)
plot_panel(axes['n'], lc4_data, 'SL_to_TL_20percent', 'LC4 - 20%', show_xticks=True)
plot_panel(axes['O'], lc5_data, 'SL_to_TL_20percent', 'LC5 - 20%', show_xticks=True)

plt.suptitle('SL/TL Ratio Heatmaps: All Landcovers by Percentile Thresholds', fontsize=16, y=0.95)
plt.tight_layout()

# Save plot
outpath = '/Users/varyabazilova/Desktop/paper2/202406_modelruns/processing_pipeline/testplots_by_claude/'
plt.savefig(outpath + 'sl_tl_ratio_heatmaps_landcover1_vs_2.png', dpi=300, bbox_inches='tight')
plt.show()