import json

PRICES_JSON_PATH = 'output/prices_test_new3.json'


def get_data(path=PRICES_JSON_PATH):
    # Load data
    with open('data/items.json') as json_file:
        data = json.load(json_file)

    try:
        with open(PRICES_JSON_PATH, 'r') as json_file:
            prices = json.load(json_file)
    except FileNotFoundError:
        prices = []

    
    return data, prices