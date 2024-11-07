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
            time_s = (round_index + 1) * 60 + 5  # Adjust the first hill score to be at 65 seconds
            transformed_data.append({
                'match_id': match_id,
                'map': map_name,
                'hill_num': hill_num,
                'time_s': time_s,
                'team': team_name,
                'score': round_score
            })

# Create a new DataFrame from the transformed data
transformed_df = pd.DataFrame(transformed_data)

# Initialize an empty list to store the per-second data
per_second_data = []

# Iterate through the transformed DataFrame and create per-second data
for index, row in transformed_df.iterrows():
    match_id = row['match_id']
    map_name = row['map']
    hill_num = row['hill_num']
    team = row['team']
    score = row['score']
    time_s = row['time_s']
    for second in range(time_s - 59, time_s):
        if second < 5:
            per_second_data.append({
                'match_id': match_id,
                'map': map_name,
                'hill_num': 0,  # Label the first 5 seconds as hill_num = 0
                'time_s': second,
                'team': team,
                'score': 0
            })
        else:
            per_second_data.append({
                'match_id': match_id,
                'map': map_name,
                'hill_num': hill_num,
                'time_s': second,
                'team': team,
                'score': 0
            })
    per_second_data.append({
        'match_id': match_id,
        'map': map_name,
        'hill_num': hill_num,
        'time_s': time_s,
        'team': team,
        'score': score
    })

# Create a new DataFrame from the per-second data
per_second_df = pd.DataFrame(per_second_data)

# Extrapolate the scores for each second
per_second_df['cumulative_score'] = per_second_df.groupby(['match_id', 'team'])['score'].cumsum()
# per_second_df['extrapolated_score'] = per_second_df.groupby(['match_id', 'team'])['cumulative_score'].apply(lambda x: x / 60)

# Save the per-second scores to a CSV file
## filter to only match_id = 'ab7e12d2-8217-5561-b6c8-927431692315'
per_second_df = per_second_df[per_second_df['match_id'] == 'ab7e12d2-8217-5561-b6c8-927431692315']
per_second_df.to_csv('/workspaces/cwl-data/per_second_scores.csv', index=False)

## print the per-second scores
print(per_second_df.head(65))

print("Per-second scores saved to 'per_second_scores.csv'")
