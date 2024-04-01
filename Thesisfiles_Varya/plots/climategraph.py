import os
import pandas as pd
import matplotlib.pyplot as plt

# Path to the directory containing the files
directory_path = "D:\\climatedata\\merge\\mustang"

# List all files in the directory
files = os.listdir(directory_path)

# Filter only the CSV files
csv_files = [file for file in files if file.endswith(".met")]

# Define the date range for filtering
start_date = pd.to_datetime("1951-01-01")
end_date = pd.to_datetime("1986-12-31")

print('Cellnr\tmavgpr\tmavgtemp')

# Loop over each CSV file
for csv_file in csv_files:
    # Extract the number between the dots in the file name
    plot_number = ''.join(filter(str.isdigit, csv_file))

    # Construct the full path to the CSV file
    file_path = os.path.join(directory_path, csv_file)

    # Load your CSV data
    df = pd.read_csv(file_path)

    # Convert the 'D' column to datetime format and set it as the index
    df['D'] = pd.to_datetime(df['D'])
    
    # Filter data based on the specified date range
    df = df[(df['D'] >= start_date) & (df['D'] <= end_date)]

    # Set the filtered 'D' column as the index
    df.set_index('D', inplace=True)

    # Resample to monthly frequency and calculate mean temperature and sum of precipitation
    monthly_data = df.resample('M').agg({'Ta': 'mean', 'Pr': 'sum'})

    # Group by month and calculate average temperature and precipitation over the years
    average_monthly_data = monthly_data.groupby(monthly_data.index.month).agg({'Ta': ['mean', 'std'], 'Pr': ['mean', 'std']})

    # Print the number between the dots in the file name, followed by the values separated by \t
    monthly_avg_precipitation = average_monthly_data['Pr']['mean'].mean()
    monthly_avg_temperature = average_monthly_data['Ta']['mean'].mean()
   # yearly_avg_temperature = df.resample('Y').agg({'Ta': 'mean'}).mean()['Ta']
    print(f"{plot_number}\t{monthly_avg_precipitation:.2f}\t{monthly_avg_temperature:.2f}")

    # Plot the monthly average temperature and precipitation with variability
    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Month')
    ax1.set_ylabel('Average Precipitation (mm)', color='tab:blue')
    ax1.bar(average_monthly_data.index, average_monthly_data['Pr']['mean'], color='tab:blue', alpha=0.7, label='Precipitation')
    ax1.errorbar(average_monthly_data.index, average_monthly_data['Pr']['mean'], yerr=average_monthly_data['Pr']['std'], linestyle='None', color='tab:blue')

    # Create a second y-axis for temperature
    ax2 = ax1.twinx()
    ax2.set_ylabel('Average Temperature (°C)', color='tab:red')
    ax2.plot(average_monthly_data.index, average_monthly_data['Ta']['mean'], color='tab:red', linestyle='-', marker='o', label='Temperature')
    ax2.errorbar(average_monthly_data.index, average_monthly_data['Ta']['mean'], yerr=average_monthly_data['Ta']['std'], linestyle='None', color='tab:red')

    # Set y-axis limits for precipitation
    ax1.set_ylim(0, 900)  # Adjust the limit as needed

    # Set y-axis limits for temperature
    ax2.set_ylim(-20, 15)  # Adjust the limits as needed

    # Add legends
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Set plot title
    plt.title(f'Monthly Average Precipitation and Temperature ({plot_number}) with Variability')

    # Save the plot to a file (optional)
    #plt.savefig(f"plot_{plot_number}.png")

    # Show the plot (optional, you can comment this out if you want to save plots only)
    plt.show()
