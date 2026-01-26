import pandas as pd
import numpy as np

# --- 0. Setup and Data Generation ---
FILE_PATH = 'D:/python/python/vs code/Cognifyz_intern/cleaned_train_data.csv'

def generate_sample_data(num_rows=1000):
    """Creates a synthetic dataset for the train operations task."""
    np.random.seed(42)
    stations = ['DELHI', 'MUMBAI', 'CHENNAI', 'KOLKATA', 'PUNE', 'HYDERABAD']
    days_options = ['MON,TUE,WED,THU,FRI', 'SAT,SUN', 'DAILY', 'MON,WED,FRI', 'SAT']
    data = {
        'Train_ID': [f'T{i:04}' for i in range(num_rows)],
        'Source_Station': np.random.choice(stations, num_rows),
        'Destination_Station': np.random.choice(stations, num_rows),
        'Operating_Days': np.random.choice(days_options, num_rows, p=[0.4, 0.2, 0.1, 0.2, 0.1]),
        'Critical_Info': np.random.choice(['A', 'B', 'C', np.nan], num_rows, p=[0.7, 0.1, 0.1, 0.1])
    }
    df = pd.DataFrame(data)
    df = df[df['Source_Station'] != df['Destination_Station']].reset_index(drop=True)
    return df

try:
    # Attempt to load your real data (Uncomment and replace 'your_train_data.csv')
    # df = pd.read_csv('your_train_data.csv')
    df = generate_sample_data(1000) # Using sample data for demonstration
except FileNotFoundError:
    print("Warning: Data file not found. Using generated sample data.")
    df = generate_sample_data(1000)

print("--- Level 1: Data Exploration and Basic Operations Started ---")

## Task 1.1: Load and Inspect Data [cite: 4, 5]
# Load the dataset and display the first 10 rows [cite: 4]
print("\n## Task 1.1: Inspection")
print("First 10 Rows:")
print(df.head(10))

# Understand the basic structure of the data, including data types and missing values [cite: 5]
print("\nData Structure and Types:")
df.info(verbose=False, memory_usage="deep")
print("\nMissing Value Counts Before Cleaning:")
print(df.isnull().sum())

## Task 1.2: Basic Statistics [cite: 7, 8]
print("\n## Task 1.2: Basic Statistics")

# Calculate basic statistics such as the number of trains, unique source stations, and unique destination stations [cite: 7]
total_trains = len(df)
unique_sources = df['Source_Station'].nunique()
unique_destinations = df['Destination_Station'].nunique()
print(f"Total Number of Trains: {total_trains}")
print(f"Unique Source Stations: {unique_sources}")
print(f"Unique Destination Stations: {unique_destinations}")

# Find the most common source and destination stations [cite: 8]
most_common_source = df['Source_Station'].mode()[0]
most_common_destination = df['Destination_Station'].mode()[0]
print(f"Most Common Source Station: {most_common_source}")
print(f"Most Common Destination Station: {most_common_destination}")

## Task 1.3: Data Cleaning [cite: 10, 11]
print("\n## Task 1.3: Data Cleaning")

# Identify and handle missing values in the dataset [cite: 10]
# Filling 'Critical_Info' NaN values with 'UNKNOWN'
df['Critical_Info'].fillna('UNKNOWN', inplace=True)
print(f"Missing values in 'Critical_Info' after handling: {df['Critical_Info'].isnull().sum()}")

# Standardize the format of station names (e.g., make all names uppercase) [cite: 11]
df['Source_Station'] = df['Source_Station'].astype(str).str.upper()
df['Destination_Station'] = df['Destination_Station'].astype(str).str.upper()
print("Station names standardized to uppercase.")

# Save the cleaned data for Level 2
df.to_csv(FILE_PATH, index=False)
print(f"\nCleaned data saved to {FILE_PATH} for use by Level 2.")
print("--- Level 1 Complete ---")