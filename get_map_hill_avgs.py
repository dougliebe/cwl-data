import pandas as pd
import os
import json

# Define the path to the output folder
output_folder = '/workspaces/cwl-data/output/structured-2018-04-08-proleague1'

# Initialize an empty list to store the data
data = []

# Loop through all files in the output folder
for filename in os.listdir(output_folder):
    if filename.endswith('.json'):
        file_path = os.path.join(output_folder, filename)
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            data.append(json_data)

# Create a DataFrame from the list of data
df = pd.DataFrame(data)

# Filter only the mode = 'Hardpoint'
df = df[df['mode'] == 'Hardpoint']

# Initialize an empty list to store the transformed data
transformed_data = []

# Iterate through the DataFrame and transform the data
for index, row in df.iterrows():
    match_id = row['id']
    map_name = row['map']
    duration = row['duration_ms']
    hp_hill_names = row['hp_hill_names']
    num_hills = len(hp_hill_names)
    for team in row['teams']:
        team_name = team['name']
        teams = row['teams']
        opponent_team_name = next(t['name'] for t in teams if t['name'] != team_name)        
        for round_index, round_score in enumerate(team['round_scores']):
            hill_num = (round_index % num_hills) + 1
            transformed_data.append({
                'match_id': match_id,
                'map': map_name,
                'duration_ms': duration,
                'team': team_name,
                'opponent_team': opponent_team_name,
                'hill_num': hill_num,
                'round_score': round_score
            })

# Create a new DataFrame from the transformed data
transformed_df = pd.DataFrame(transformed_data)

# Calculate the average hill score for each map and hill
average_hill_scores = transformed_df.groupby(['map', 'hill_num'])['round_score'].mean().reset_index()

# Save the average hill scores to a CSV file
average_hill_scores.to_csv('/workspaces/cwl-data/average_hill_scores_by_map_and_hill.csv', index=False)

## print the average hill scores
print(average_hill_scores)

print("Average hill scores saved to 'average_hill_scores_by_map_and_hill.csv'")
