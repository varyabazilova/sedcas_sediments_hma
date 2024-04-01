import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

#%matplotlib inline

# Specify the directory containing the .out files
directory = r"D:\outputs_sedcas\heatmap\bagrot\cell9\sed"

# Get a list of all files with a .out extension in the directory
out_files = [file for file in os.listdir(directory) if file.endswith('.out')]

# Sort the out_files list based on the file numbers
out_files.sort(key=lambda x: int(x.split('.')[1].split('.')[0]))

# Iterate over each .out file
for out_file in out_files:
    # Extract the number between two underscores from the filename
    file_number = out_file.split('.')[1].split('.')[0]

    # Construct the full path to the current file
    file_path = os.path.join(directory, out_file)

    # Read the sediment data from a CSV file and convert it to a DataFrame
    path = pd.read_csv(file_path, index_col=0)
    sediments = path

    # Set the desired time frame
    start_date = '1951-09-01T00:00:00.000000000'
    end_date = '2022-09-30T23:00:00.000000000'

    # Convert the 'D' index to datetime
    sediments.index = pd.to_datetime(sediments.index)

    # Filter the DataFrame based on the desired time frame
    sediments = sediments[(sediments.index >= start_date) & (sediments.index <= end_date)]

    # Unit conversion and creating a new DataFrame
    #area = 4.83
    #cf = (area * 10**6) * 10**-3  # km2 to m2 and mm to m
    sediments_area = pd.DataFrame()
    sediments_area['Qstl'] = sediments.Qstl #* cf
    sediments_area['Qdftl'] = sediments.Qdftl #* cf
    sediments_area.index = pd.to_datetime(sediments_area.index)

    # Resampling data to monthly frequency and calculating monthly means
    sym = sediments_area.resample('m').sum()
    symm_westernhimal = sym.groupby(by=sym.index.month).mean()
    symm_westernhimal = symm_westernhimal.reset_index()

    # Plotting the data using matplotlib
    fig, ax = plt.subplots(figsize=(10, 5))
    width = 0.2
    ax.bar(x=symm_westernhimal.D + 0.1, height=symm_westernhimal.Qdftl, width=width, label='only DF sediments', alpha=0.7, color='chartreuse')
    ax.bar(x=symm_westernhimal.D - 0.1, height=symm_westernhimal.Qstl, width=width, label='all sediments', alpha=0.7, color='dodgerblue')

    ax.set_xticks(symm_westernhimal.D)
    ax.set_xticklabels(symm_westernhimal.D, fontsize=15)
    ax.set_xlabel('Months', fontsize=15)
    ax.legend(fontsize=15)
    ax.tick_params(axis='y', labelsize=15)

    # Calculating and printing summary statistics
    total_sediment_yield = symm_westernhimal['Qdftl'].sum() + symm_westernhimal['Qstl'].sum()
    debrisflow_seiment_yield = symm_westernhimal['Qdftl'].sum()
    nondebrisflow_seiment_yield = symm_westernhimal['Qstl'].sum()
    maxdebrisflow_seiment_yield = symm_westernhimal['Qdftl'].max()
    maxnondebrisflow_seiment_yield = symm_westernhimal['Qstl'].max()

    print(f'Cell {file_number}:\t{total_sediment_yield:.2f}\t{debrisflow_seiment_yield}')
    #print(f'Cell {file_number}:\t{total_sediment_yield:.2f}\t{debrisflow_seiment_yield}\t{nondebrisflow_seiment_yield}\t{maxdebrisflow_seiment_yield}\t{maxnondebrisflow_seiment_yield}')
    #print(f'Total Sediment Yield Month Mean: {total_sediment_yield:.2f} ')
    #print(f'Total Sediment yield month mean debrisflow: {debrisflow_seiment_yield} m³')
    #print(f'Total Sediment yield month mean nondebrisflow: {nondebrisflow_seiment_yield} m³')
    #print(f'Max Sediment yield month mean debrisflow: {maxdebrisflow_seiment_yield} m³')
    #print(f'Max Sediment yield month mean nondebrisflow: {maxnondebrisflow_seiment_yield} m³')

    ax.set_ylabel('Sediment Yield (mm)', fontsize=15)
    ax.set_title(f'Sediment Yield Over Time - cell {file_number}', fontsize=18)
    fig.tight_layout()

    # Save the figure with a filename that includes the file_number
    fig.savefig(f'sed_yeld_{file_number}.pdf', bbox_inches='tight')

    # Display the plot
    plt.show()

    # Close the figure to start with a new one for the next iteration
    #plt.close(fig)
