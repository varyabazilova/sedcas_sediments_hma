# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 10:22:18 2025

@author: 6935737
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# Input directory path
input_dir = r"D:\Thesisfiles_Varya\Thesisfiles_Varya\climate\finalclimatefiles\bagrot"

# Output directory path (create it if it doesn't exist)
output_dir = r"D:\Thesisfiles_Varya\Thesisfiles_Varya\climate\finalclimatefiles2\bagrot"
os.makedirs(output_dir, exist_ok=True)

# Function to process a single .met file
def process_met_file(input_file_path, output_file_path):
    try:
        # Read the data (adjust separator if needed)
        df = pd.read_csv(input_file_path, sep=',') # added the separator

        # Convert 'D' to datetime
        df['D'] = pd.to_datetime(df['D'], format='%Y-%m-%d %H:%M:%S')

        # Shift 'Rsw' for hourly calculation
        df['Rsw_shifted'] = df['Rsw'].shift(-1)

        # Calculate hourly radiation
        df['Hourly_Radiation'] = df.groupby(df['D'].dt.date)['Rsw_shifted'].diff().fillna(df['Rsw_shifted'])

        # Create a new DataFrame for shifted data
        shifted_df = pd.DataFrame()
        shifted_df['D'] = df['D'] + pd.DateOffset(hours=1)
        shifted_df['Rsw'] = df['Rsw'].shift(-1)
        shifted_df['Hourly_Radiation'] = df['Hourly_Radiation'].shift(0)

        # Merge shifted data with original data for other columns
        df = pd.merge(shifted_df, df[['Pr', 'Ta', 'N', 'D']], on='D', how='left')

        # Set 'D' as index
        df.set_index('D', inplace=True)

        # Select and save columns
        selected_columns = ['Rsw', 'Hourly_Radiation', 'Pr', 'Ta', 'N']
        df[selected_columns].to_csv(output_file_path, header=selected_columns)

        print(f"File processed: {os.path.basename(input_file_path)} -> {os.path.basename(output_file_path)}")

    except FileNotFoundError:
        print(f"Error: Input file not found at: {input_file_path}")
    except pd.errors.ParserError as e:
        print(f"Error parsing file {input_file_path}: {e}")
        print("Check if the file is correctly formatted and if the separator argument in pd.read_csv is correct.")
    except KeyError as e:
        print(f"KeyError in file {input_file_path}: Column '{e.args[0]}' not found.")
        print("Check if the column names in the file match the code.")
    except Exception as e:
        print(f"An unexpected error occurred for file {input_file_path}: {e}")

# Loop through all .met files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".met"):
        input_file_path = os.path.join(input_dir, filename)
        output_file_path = os.path.join(output_dir, filename)
        process_met_file(input_file_path, output_file_path)

print("All files processed!")