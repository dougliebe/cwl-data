## extract_tabular_info.py
import os

def extract_tabular_info(json_file_path):
    import json


    with open(json_file_path, 'r') as file:
        data = json.load(file)

    extracted_info = {
        "title": data.get("title"),
        "platform": data.get("platform"),
        "id": data.get("id"),
        "series_id": data.get("series_id"),
        "start_time_s": data.get("start_time_s"),
        "end_time_s": data.get("end_time_s"),
        "duration_ms": data.get("duration_ms"),
        "mode": data.get("mode"),
        "map": data.get("map"),
        "rounds": data.get("rounds"),
        "hp_hill_names": data.get("hp_hill_names"),
        "hp_hill_rotations": data.get("hp_hill_rotations"),
        "teams": [
            {
                "name": team.get("name"),
                "score": team.get("score"),
                "is_victor": team.get("is_victor"),
                "round_scores": team.get("round_scores"),
                "side": team.get("side")
            } for team in data.get("teams", [])
        ]
    }

    return extracted_info

# Example usage
# Get the name of the first file in the ./output directory
output_dir = './output'
first_file_name = next(os.scandir(output_dir)).name

# Update the json_file_path with the first file name
json_file_path = os.path.join(output_dir, first_file_name)
# json_file_path = 'output/structured-2018-04-08-proleague1/[json-file].json'
info = extract_tabular_info(json_file_path)
print(info)

## init extract_tabular_info.py
