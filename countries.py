import os
import json


def get_countries():
    """ 
    Retrieve a list of countries from a JSON file.

    Returns
    --------------
    list
        A list of country names.
    """
    path = os.path
    current_dir = path.dirname(__file__)
    data_path = path.join(current_dir, 'data', 'countries.json')

    with open(data_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
        return data.get('countries', [])
