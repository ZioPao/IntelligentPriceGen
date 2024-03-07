import json

PRICES_JSON_PATH = 'output/prices_test_new.json'


def get_data():
    # Load data
    with open('data/items.json') as json_file:
        data = json.load(json_file)

    try:
        with open(PRICES_JSON_PATH, 'r') as json_file:
            prices = json.load(json_file)
    except FileNotFoundError:
        prices = []

    
    return data, prices