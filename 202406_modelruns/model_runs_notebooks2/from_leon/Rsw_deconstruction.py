import pandas as pd
import matplotlib.pyplot as plt
import os

# Input file path
input_file_path = r"D:\Thesisfiles_Varya\Thesisfiles_Varya\climate\finalclimatefiles\Bagrot\climatecell.9.csv"

# Output file path
output_file_path = r"D:\Thesisfiles_Varya\Thesisfiles_Varya\climate\finalclimatefiles2\bagrot\climatecell.9.1.csv"

try:
    # Read the data
    df = pd.read_csv(input_file_path)

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

    # Plotting (Optional)
    plt.figure(figsize=(12, 6))
    # ... (plotting code remains the same)
    plt.tight_layout()
    plt.show()

    # Set 'D' as index
    df.set_index('D', inplace=True)

    # Create output directory
    output_dir = os.path.dirname(output_file_path)
    os.makedirs(output_dir, exist_ok=True)

    # Select and save columns
    selected_columns = ['Rsw', 'Hourly_Radiation', 'Pr', 'Ta', 'N']
    df[selected_columns].to_csv(output_file_path, header=selected_columns)

    print(f"File saved to: {output_file_path}")

except FileNotFoundError:
    print(f"Error: Input file not found at: {input_file_path}")
except pd.errors.ParserError:
    print(f"Error: Could not parse the input file.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")