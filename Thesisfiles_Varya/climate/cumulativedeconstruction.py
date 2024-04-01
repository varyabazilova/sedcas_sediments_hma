import pandas as pd
import matplotlib.pyplot as plt

# Replace 'D:\climatedata\merge\Pr.csv' with the actual path to your CSV file
file_path = 'D:\climatedata\merge\Pr.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Convert the 'D' column to datetime format
#df['D'] = pd.to_datetime(df['D'], format='%d/%m/%Y %H:%M')
df['D'] = pd.to_datetime(df['D'], format='%Y-%m-%d %H:%M:%S')

print(df[['D', 'Pr']])

df['Pr'] = df['Pr'].shift(-1)

# Calculate the hourly precipitation by subtracting the previous day's cumulative value
# and filling the first row of each day with the original cumulative value
df['Hourly_Precipitation'] = df.groupby(df['D'].dt.date)['Pr'].diff().fillna(df['Pr'])

# Shift all the data forward by one hour
df['D'] = df['D'] + pd.DateOffset(hours=1)
df['Pr'] = df['Pr'].shift(1)
df['Hourly_Precipitation'] = df['Hourly_Precipitation'].shift(1)

# Display the result
print(df[['D', 'Hourly_Precipitation']])

# Plot the 'Pr' column from the original DataFrame
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(df['D'], df['Pr'], label='Original Data')
plt.title('Original DataFrame (Shifted)')
plt.xlabel('Date')
plt.ylabel('Cumulative Precipitation')
plt.legend()

# Plot the 'Hourly_Precipitation' column from the new DataFrame
plt.subplot(2, 1, 2)
plt.plot(df['D'], df['Hourly_Precipitation'], label='Hourly Precipitation')
plt.axhline(0, color='black', linestyle='--', linewidth=1, label='Zero Line')
plt.title('Hourly Precipitation DataFrame (Shifted)')
plt.xlabel('Date')
plt.ylabel('Hourly Precipitation')
plt.legend()

plt.tight_layout()
plt.show()

# Set 'D' column as the index
df.set_index('D', inplace=True)

# Save the DataFrame with hourly precipitation to a new CSV file
df[['Hourly_Precipitation']].to_csv('D:\climatedata\merge\HPr.csv', header=['Pr'])