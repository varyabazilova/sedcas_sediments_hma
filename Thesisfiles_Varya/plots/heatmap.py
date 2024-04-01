import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
file_path = r"D:\outputs_sedcas\heatmap\bagrot\cell9\averagebagrot.csv"
df = pd.read_csv(file_path)

# Pivot the DataFrame to create the heatmap data structure
heatmap_data = df.pivot_table(values='debri', index='veg', columns='glacier')

# Reverse the order of rows in the DataFrame
heatmap_data = heatmap_data.iloc[::-1]

# Create a heatmap using seaborn with reversed y-axis labels and values
plt.figure(figsize=(12, 8))

# Set custom y-axis tick labels and reverse the order
custom_y_labels = ['7.5', '12.5', '17.5', '22.5', '27.5', '32.5']
heatmap = sns.heatmap(heatmap_data, cmap='Reds', annot=False, fmt=".2f", linewidths=.5, yticklabels=custom_y_labels, annot_kws={"size": 32})

# Set custom x-axis tick labels font size
plt.xticks(fontsize=30)  # Adjust the fontsize as needed

# Set custom y-axis tick labels font size and reverse the order
plt.yticks(ticks=plt.yticks()[0][::-1], labels=custom_y_labels, fontsize=28)  # Adjust the fontsize as needed
plt.xticks(fontsize=28)
# Set title font size
#plt.title('Heatmap of Debris vs. Glacier and Veg', fontsize=30)  # Adjust the fontsize as needed

# Set x-axis and y-axis label font sizes
plt.xlabel('Glacier (%)', fontsize=32)
plt.ylabel('Vegetation (%)', fontsize=32)

# Adjust colorbar tick label font size
cbar = heatmap.collections[0].colorbar
cbar.ax.tick_params(labelsize=28)  # Adjust the fontsize as needed

# Adjust text annotation font size
annot_font_size = 28

# Add colorbar label with custom font
cbar_label_text = 'Debris flow Yield (mm)'
cbar.set_label(cbar_label_text, fontsize=30, fontproperties={'size': 30})

plt.show()
