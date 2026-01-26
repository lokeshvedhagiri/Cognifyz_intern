import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Matplotlib style for better visualization aesthetics
sns.set_style('whitegrid')

# --- 0. Setup and Data Loading ---
INPUT_FILE_PATH = 'D:/python/python/vs code/Cognifyz_intern/enriched_train_data.csv'

try:
    df = pd.read_csv(INPUT_FILE_PATH)
except FileNotFoundError:
    print(f"Error: Required enriched data file not found at {INPUT_FILE_PATH}. Run 'level_2_transformation.py' first.")
    exit()

print("--- Level 3: Advanced Data Analysis Started ---")

## Task 3.1: Pattern Analysis [cite: 23, 24]
print("\n## Task 3.1: Pattern Analysis")

# Analyze the distribution of train journeys throughout the week. Visualize the results using bar plots [cite: 23]
category_counts = df['Day_Category'].value_counts()
print("\nDistribution by Day Category:")
print(category_counts)

# Bar Plot Visualization
plt.figure(figsize=(9, 5))
sns.barplot(x=category_counts.index, y=category_counts.values, palette="rocket")
plt.title('Distribution of Train Journeys by Operating Day Category')
plt.xlabel('Operating Day Category')
plt.ylabel('Number of Unique Trains')
plt.show()

# Identify patterns or trends in the train operations based on source and destination stations [cite: 24]
route_counts = df.groupby(['Source_Station', 'Destination_Station']).size().sort_values(ascending=False).reset_index(name='Count')
print("\nTop 5 Most Frequent Routes (Source -> Destination):")
print(route_counts.head())

## Task 3.2: Correlation and Insights [cite: 26, 27]
print("\n## Task 3.2: Correlation and Insights")

# Explore if there is any correlation between the number of trains and specific days of the week [cite: 26]
# We use the Day_Category distribution (from 3.1) and the Operating_Days_Count.
avg_daily_op_by_category = df.groupby('Day_Category')['Operating_Days_Count'].mean().sort_values(ascending=False)
print("\nAverage Operating Days Count by Day Category:")
print(avg_daily_op_by_category)

# The large difference in 'Count' (from 3.1) between 'Weekday Only' and 'Weekend Only' (if present) 
# shows a strong correlation where the majority of individual train services are geared towards weekdays.

# Provide insights and recommendations based on the analysis [cite: 27]
top_route_source = route_counts.iloc[0]['Source_Station']
top_route_dest = route_counts.iloc[0]['Destination_Station']
highest_category = category_counts.index[0]
highest_category_count = category_counts.iloc[0]

print("\n--- Insights and Recommendations [cite: 27] ---")
print(f"**Insight 1 (Operational Focus):** The vast majority ({highest_category_count}) of train services are categorized as '{highest_category}', suggesting a high concentration of operational resources on routes serving most of the week.")
print(f"**Insight 2 (Network Demand):** The route from **{top_route_source}** to **{top_route_dest}** is the most frequented route, indicating the highest passenger/freight demand in the network.")
print(f"**Recommendation 1 (Capacity):** Increase capacity or introduce parallel services on the top route ({top_route_source} to {top_route_dest}) to alleviate congestion and maximize revenue.")
print(f"**Recommendation 2 (Scheduling):** Review the schedules for 'Weekend Only' routes to assess if increasing their frequency on high-demand corridors could balance the network load and capture additional weekend travel market.")

print("--- Level 3 Complete ---")