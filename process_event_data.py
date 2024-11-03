import json

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

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

def extract_event_data(data):
    events = data.get('events', [])
    processed_events = []

    for event in events:
        event_type = event.get('type')
        if event_type != 'death':
            continue

        time_ms = event.get('time_ms')
        round_number = event.get('round')
        round_time_ms = event.get('round_time_ms')
        event_data = event.get('data', {})

        processed_event = {
            'title': data.get('title'),
            'game_id': data.get('id'),
            'mode': data.get('mode'),
            'map': data.get('map'),
            'type': event_type,
            'time_ms': time_ms,
            'round': round_number,
            'round_time_ms': round_time_ms,
            'victim_id': event_data.get('id'),
            'attacker_id': event_data.get('attacker', {}).get('id'),
            'pos_x': event_data.get('pos', {}).get('x'),
            'pos_y': event_data.get('pos', {}).get('y'),
            'attacker_pos_x': event_data.get('attacker', {}).get('pos', {}).get('x'),
            'attacker_pos_y': event_data.get('attacker', {}).get('pos', {}).get('y'),
            'means_of_death': event_data.get('attacker', {}).get('means_of_death')
        }
        processed_events.append(processed_event)

    return processed_events

def main():
    file_path = 'output/structured-2018-04-08-proleague1/structured-1516744182-1cc51f61-d9bd-5d5e-b7e2-e5945e863ff9.json'
    data = read_json_file(file_path)
    processed_events = extract_event_data(data)

    for event in processed_events:
        print(event)

if __name__ == "__main__":
    main()