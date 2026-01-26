import pandas as pd
import numpy as np

# --- 0. Setup and Data Loading ---
INPUT_FILE_PATH = 'D:/python/python/vs code/Cognifyz_intern/cleaned_train_data.csv'
OUTPUT_FILE_PATH = 'D:/python/python/vs code/Cognifyz_intern/enriched_train_data.csv'

try:
    df = pd.read_csv(INPUT_FILE_PATH)
except FileNotFoundError:
    print(f"Error: Required cleaned data file not found at {INPUT_FILE_PATH}. Run 'level_1_exploration.py' first.")
    exit()

print("--- Level 2: Data Transformation and Aggregation Started ---")

## Task 2.1: Data Filtering [cite: 14, 15]
print("\n## Task 2.1: Data Filtering")

# Filter the data to show trains that operate only on Saturdays [cite: 14]
# Note: This filters for trains whose 'Operating_Days' string includes 'SAT'
saturday_trains_df = df[df['Operating_Days'].str.contains('SAT', case=False, na=False)].copy()
print(f"Number of trains operating on Saturdays: {len(saturday_trains_df)}")

# Extract and create a new dataframe for trains that start from a specific station (e.g., DELHI) [cite: 15]
specific_station = 'DELHI' 
delhi_trains_df = df[df['Source_Station'] == specific_station].copy()
print(f"Number of trains originating from {specific_station}: {len(delhi_trains_df)}")

## Task 2.2: Grouping and Aggregation [cite: 17, 18]
print("\n## Task 2.2: Grouping and Aggregation")

# Group the data by source station and count the number of trains originating from each station [cite: 17]
trains_per_source = df.groupby('Source_Station').size().reset_index(name='Number_of_Trains')
print("Top 5 Source Stations by Train Count:")
print(trains_per_source.sort_values(by='Number_of_Trains', ascending=False).head())

# Helper function to count operating days (needed for Task 2.2 and 3.1)
def count_operating_days(days_str):
    """Counts the number of operating days based on the string."""
    days_str = str(days_str).upper()
    if 'DAILY' in days_str:
        return 7
    return len([d for d in ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'] if d in days_str])

df['Operating_Days_Count'] = df['Operating_Days'].apply(count_operating_days)

# Find the average number of trains per day for each source station [cite: 18]
trains_per_day_agg = df.groupby('Source_Station').agg(
    Total_Trains=('Train_ID', 'count'),
    Total_Daily_Ops=('Operating_Days_Count', 'sum')
).reset_index()

# Calculation: Total daily operations originating from source / Total trains from that source
trains_per_day_agg['Avg_Trains_Per_Day'] = trains_per_day_agg['Total_Daily_Ops'] / trains_per_day_agg['Total_Trains']
print("\nTop 5 Source Stations by Average Trains Per Day (Total Daily Ops / Total Trains):")
print(trains_per_day_agg[['Source_Station', 'Avg_Trains_Per_Day']].sort_values(by='Avg_Trains_Per_Day', ascending=False).head())

## Task 2.3: Data Enrichment [cite: 20]
print("\n## Task 2.3: Data Enrichment")

# Add a new column that categorizes trains based on their operating days (e.g., 'Weekday', 'Weekend') [cite: 20]
def categorize_train_day(days):
    """Categorizes trains as 'Weekend', 'Weekday', or 'Mixed' based on operating days."""
    days = str(days).upper()
    is_weekend = 'SAT' in days or 'SUN' in days
    is_weekday = 'MON' in days or 'TUE' in days or 'WED' in days or 'THU' in days or 'FRI' in days or 'DAILY' in days
    
    if is_weekend and is_weekday:
        return 'Mixed/Daily'
    elif is_weekend:
        return 'Weekend Only'
    elif is_weekday:
        return 'Weekday Only'
    return 'Other'

df['Day_Category'] = df['Operating_Days'].apply(categorize_train_day)
print("New 'Day_Category' column added.")
print(df[['Operating_Days', 'Day_Category']].head())

# Save the enriched data for Level 3
df.to_csv(OUTPUT_FILE_PATH, index=False)
print(f"\nEnriched data saved to {OUTPUT_FILE_PATH} for use by Level 3.")
print("--- Level 2 Complete ---")