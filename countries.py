import json
import os

def get_countries():
    current_dir = os.path.dirname(__file__)
    data_path = os.path.join(current_dir, 'data', 'countries.json')

    with open(data_path, 'r') as file:
        data = json.load(file)
        return data.get('countries', [])
