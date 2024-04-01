import os
import pandas as pd
import matplotlib.pyplot as plt

# Directory containing the .out files
directory_path = r"D:\outputs_sedcas\langtang\[0.075,0.925,0.0]\hydro"

# Initialize empty DataFrames to store aggregated data for glacier melt and Q
agg_df_melt = pd.DataFrame()
agg_df_q = pd.DataFrame()

# Loop through all .out files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith(".out"):
        file_path = os.path.join(directory_path, filename)
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Convert the 'D' column to a datetime format
        df['D'] = pd.to_datetime(df['D'])

        # Extract the month and year from the datetime column
        df['Month'] = df['D'].dt.month
        df['Year'] = df['D'].dt.year

        # Group by month and year, calculate the sum for each month, and then average over the years for glacier melt
        monthly_avg_melt = df.groupby(['Month', 'Year'])['melt'].sum().groupby('Month').mean()

        # Print the yearly average glacier melt for each file
        yearly_avg_melt = df.groupby('Year')['melt'].sum().mean()
        #print(f"File: {filename}, Yearly Average Glacier Melt: {yearly_avg_melt}")
        print((f"{filename}\t{yearly_avg_melt}"))

        # Append the results to the aggregated DataFrames
        agg_df_melt = pd.concat([agg_df_melt, monthly_avg_melt], axis=1)
        agg_df_q = pd.concat([agg_df_q, df.groupby(['Month', 'Year'])['Q'].sum().groupby('Month').mean()], axis=1)

# Transpose the aggregated DataFrames for plotting
agg_df_melt = agg_df_melt.T
agg_df_q = agg_df_q.T

# Define a list of month abbreviations
month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Plot all lines for glacier melt in one plot
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(agg_df_melt.columns, agg_df_melt.values.T, marker='o')
plt.xlabel('Month')
plt.xticks(range(1, 13), month_labels)  # Use month abbreviations as x-axis tick labels
plt.ylabel('Average Monthly Glacier Melt (mm)')
plt.title('Average Monthly Glacier Melt Over Years')
plt.legend(os.listdir(directory_path))  # Use filenames as legend labels
plt.grid(True)

# Plot all lines for Q in a second plot
plt.subplot(1, 2, 2)
plt.plot(agg_df_q.columns, agg_df_q.values.T, marker='o')
plt.xlabel('Month')
plt.xticks(range(1, 13), month_labels)  # Use month abbreviations as x-axis tick labels
plt.ylabel('Average Monthly Q')
plt.title('Average Monthly Q Over Years')
plt.legend(os.listdir(directory_path))  # Use filenames as legend labels
plt.grid(True)

plt.tight_layout()
plt.show()
