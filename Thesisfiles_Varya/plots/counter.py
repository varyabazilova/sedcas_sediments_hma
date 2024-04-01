import os
import pandas as pd

# Specify the directory containing the CSV files
folder_path = r"D:\climatedata\merge\mustang"

# Specify the time period filter
start_date = '1986-09-01'
end_date = '2022-9-30'

# Iterate over all files in the directory
for filename in os.listdir(folder_path):
    if filename.endswith(".met"):
        # Construct the full file path
        file_path = os.path.join(folder_path, filename)

        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Convert the 'D' column to a datetime format
        df['D'] = pd.to_datetime(df['D'])

        # Apply the time period filter
        df = df[(df['D'] >= start_date) & (df['D'] <= end_date)]

        # Count the number of times Qdftl is higher than 0
        count_higher_than_zero = (df['Pr'] > 5).sum()

        # Print the result for each file
        print(f"{filename}\t{count_higher_than_zero}")
