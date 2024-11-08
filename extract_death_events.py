import pandas as pd
import os
import json

# Define the path to the output folder
output_folder = '/workspaces/cwl-data/output/structured-2018-04-08-proleague1'

# Initialize an empty list to store the death events
death_events = []

# Loop through all files in the output folder
for filename in os.listdir(output_folder):
    if filename.endswith('.json'):
        file_path = os.path.join(output_folder, filename)
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            match_id = json_data.get('id')
            events = json_data.get('events', [])
            for event in events:
                if event['type'] == 'death':
                    event_data = event.copy()
                    event_data['player_id'] = event_data['data']['id']
                    event_data['attacker_id'] = event_data['data']['attacker']['id']
                    event_data['match_id'] = match_id
                    event_data.pop('data', None)  # Remove the 'data' column if it exists
                    death_events.append(event_data)

# Create a DataFrame from the list of death events
death_events_df = pd.DataFrame(death_events)

# Save the death events to a CSV file
death_events_df.to_csv('/workspaces/cwl-data/death_events.csv', index=False)

# Print the first few rows of the death events DataFrame
print(death_events_df.head())

print("Death events saved to 'death_events.csv'")
