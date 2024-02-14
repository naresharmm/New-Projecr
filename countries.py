'''Country.py
'''
import os
import json


def get_countries():
    ''' function
    '''
    path = os.path
    current_dir = path.dirname(__file__)
    data_path = path.join(current_dir, 'data', 'countries.json')

    with open(data_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
        return data.get('countries', [])
