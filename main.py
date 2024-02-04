from setup_llm import run_loop
import json


with open('data/items.json') as json_file:
    data = json.load(json_file)




dict_prices = run_loop(data=data, items_per_prompt=1)
