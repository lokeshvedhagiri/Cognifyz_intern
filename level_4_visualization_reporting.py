import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Matplotlib style for a professional look
sns.set_style('whitegrid')

# --- 0. Data Loading (Assuming enriched data from Level 2/3) ---
INPUT_FILE_PATH = 'D:/python/python/vs code/Cognifyz_intern/enriched_train_data.csv'

try:
    df = pd.read_csv(INPUT_FILE_PATH)
except FileNotFoundError:
    print(f"Error: Required enriched data file not found at {INPUT_FILE_PATH}. Please run Level 1 and 2 first.")
    exit()

# --- Re-calculate necessary aggregations from Level 2/3 for visualization ---
trains_per_source = df.groupby('Source_Station').size().reset_index(name='Number_of_Trains')
trains_per_source_sorted = trains_per_source.sort_values(by='Number_of_Trains', ascending=False)
route_counts = df.groupby(['Source_Station', 'Destination_Station']).size().sort_values(ascending=False).reset_index(name='Count')

print("--- Level 4: Data Visualization and Reporting Started ---")

print("\n## Task 4.1: Visualization")

# 1. Bar Chart: Number of Trains per Station (Top 10 Sources) 
plt.figure(figsize=(12, 6))
top_n = 10
sns.barplot(
    x='Source_Station', 
    y='Number_of_Trains', 
    data=trains_per_source_sorted.head(top_n),
    palette='viridis'
)
plt.title(f'Top {top_n} Source Stations by Total Train Count')
plt.xlabel('Source Station')
plt.ylabel('Number of Trains')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show() # 

# 2. Heatmap: Visualize Train Volume Across Top Routes (Source vs. Destination) 
# Select the top 5 sources and top 5 destinations to create a readable heatmap.
top_sources = trains_per_source_sorted['Source_Station'].head(5).tolist()
top_destinations = df['Destination_Station'].value_counts().head(5).index.tolist()

route_matrix = route_counts.pivot_table(
    index='Source_Station', 
    columns='Destination_Station', 
    values='Count', 
    fill_value=0
)

# Filter the matrix for the top stations
heatmap_data = route_matrix.loc[
    route_matrix.index.intersection(top_sources), 
    route_matrix.columns.intersection(top_destinations)
]

plt.figure(figsize=(9, 8))
sns.heatmap(
    heatmap_data, 
    annot=True, 
    fmt='d', 
    cmap='coolwarm', 
    linewidths=.5, 
    linecolor='black'
)
plt.title('Heatmap of Train Counts for Top 5 Routes')
plt.xlabel('Destination Station')
plt.ylabel('Source Station')
plt.show() #