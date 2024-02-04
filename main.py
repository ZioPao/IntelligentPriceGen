from setup_llm import run_loop
import json


with open('data/items.json') as json_file:
    data = json.load(json_file)


print("Items to consider: " + str(len(data)))

dict_prices = run_loop(data=data, items_per_prompt=10)


with open('exported_prices.json', 'w') as file:
    file.write(json.dumps(dict_prices, indent=4))

