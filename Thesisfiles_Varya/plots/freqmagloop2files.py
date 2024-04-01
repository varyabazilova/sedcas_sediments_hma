import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Specify the directories containing the files for each time period
directory_period1 = r"D:\outputs_sedcas\langtang\[0.1554,0.8446,0.0]\sed"
directory_period2 = r"D:\outputs_sedcas\langtang\[0.1554,0.8446,0.0]\sed"

# Get a list of all files in each directory
files_period1 = [file for file in os.listdir(directory_period1) if file.endswith('.out')]
files_period2 = [file for file in os.listdir(directory_period2) if file.endswith('.out')]

# Iterate over each file with the same name in both directories
for file_period1 in files_period1:
    file_period2 = next((file for file in files_period2 if file == file_period1), None)

    # Check if the file exists in both directories
    if file_period2:
        # Construct the full path to the files for each time period
        file_path_period1 = os.path.join(directory_period1, file_period1)
        file_path_period2 = os.path.join(directory_period2, file_period2)

        # Read CSV files into DataFrames for each time period
        df_period1 = pd.read_csv(file_path_period1)
        df_period2 = pd.read_csv(file_path_period2)

        # Convert the 'D' column to datetime format for each DataFrame
        df_period1['D'] = pd.to_datetime(df_period1['D'])
        df_period2['D'] = pd.to_datetime(df_period2['D'])

        # Assuming 'Qdftl' is the column in your DataFrames
        Qdftl_period1 = df_period1['Qdftl']
        Qdftl_period2 = df_period2['Qdftl']

        # Filter out zero values for each time period
        non_zero_values_period1 = Qdftl_period1[Qdftl_period1 > 0]
        non_zero_values_period2 = Qdftl_period2[Qdftl_period2 > 0]

        # Check if there are positive values to plot for both time periods
        if not (non_zero_values_period1.empty and non_zero_values_period2.empty):
            # Create subplots for frequency-magnitude and ranked curves
            fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))

            # Combine non-zero values for both time periods
            # (Note: You may want to adjust the time periods based on your specific requirements)
            # For example, you can change the date ranges as needed.
            time_period_1 = (df_period1['D'] >= '1951-01-01') & (df_period1['D'] < '1986-01-01')
            time_period_2 = (df_period2['D'] >= '1986-01-01') & (df_period2['D'] < '2022-01-01')

            non_zero_values_period1 = Qdftl_period1[time_period_1][Qdftl_period1[time_period_1] > 0]
            non_zero_values_period2 = Qdftl_period2[time_period_2][Qdftl_period2[time_period_2] > 0]

            # Check if there are positive values in the time periods for both files
            if not (non_zero_values_period1.empty and non_zero_values_period2.empty):
                # Create histograms
                hist_1, bins_1 = np.histogram(non_zero_values_period1, bins=50)
                hist_2, bins_2 = np.histogram(non_zero_values_period2, bins=50)

                # Plot frequency-magnitude curves
                axes[0].bar(bins_1[:-1], hist_1, width=(bins_1[1] - bins_1[0]), edgecolor='black', alpha=0.5, label='1951-1986')
                axes[0].bar(bins_2[:-1], hist_2, width=(bins_2[1] - bins_2[0]), edgecolor='black', alpha=0.5, label='1986-2022')
                axes[0].set_xlabel('Magnitude')
                axes[0].set_ylabel('Frequency')
                axes[0].set_title(f'Frequency-Magnitude Curve\nFile: {file_period1} vs {file_period2}')
                axes[0].legend()

                # Plot ranked curves
                ranked_values_1 = np.sort(non_zero_values_period1)[::-1]
                ranked_values_2 = np.sort(non_zero_values_period2)[::-1]
                axes[1].plot(ranked_values_1, range(1, len(ranked_values_1) + 1), marker='o', linestyle='', color='b', label='1951-1986')
                axes[1].plot(ranked_values_2, range(1, len(ranked_values_2) + 1), marker='o', linestyle='', color='r', label='1986-2022')
                axes[1].set_xscale('log')
                axes[1].set_yscale('log')
                axes[1].set_xlabel('Magnitude (Ranked)')
                axes[1].set_ylabel('Frequency (Rank)')
                axes[1].set_title(f'Ranked Curve\nFile: {file_period1} vs {file_period2}')
                axes[1].legend()

                fig.tight_layout()
                plt.show()
            else:
                print(f"No positive values to plot for files: {file_period1} and {file_period2}")
        else:
            print(f"No positive values to plot for files: {file_period1} and {file_period2}")
    else:
        print(f"Files with the same name not found in both directories: {file_period1}")
