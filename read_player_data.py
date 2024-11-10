import pandas as pd
import os
from glob import glob

# Define the directory containing the CSV files
directory = 'D:/ANALYTICS/COD/bp_data/players'

# Get a list of all CSV files in the directory
csv_files = glob(os.path.join(directory, '*.csv'))

# Read each CSV file into a DataFrame and concatenate them into a single DataFrame
player_data = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)

# Display the combined DataFrame
print(player_data.head())