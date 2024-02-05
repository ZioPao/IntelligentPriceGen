from llm_worker import LmmWorker, LmmEnum
import json
from llama_cpp import LlamaGrammar
import httpx
import tqdm


SYSTEM_MESSAGE = """\You're a tool to help make games. Always try to answer even if you think you don't have enough data"""


BASE_PROMPT = """I'm creating an economy system in a game.
I'll give you the following data in json form:
- Item Name
- Item FullType (You can understand better what it is)
- Item Weight
- Item Categories (Could be empty)
- Item BulletDefense Stat (Could be empty)
- Item Damage Stat (Could be empty)

From this data, you'll need to return ONLY its price in dollars.
Keep in mind:
- Military items, guns, and weapons should cost AT LEAST $500, but generally (especially for guns) you can go much higher. Account for other attributes, such as damage or BulletDefense
- Items listed with Category "Blunt" are weapons
- Some items can have the "BulletDefense" attribute. If it's higher than 0, the cost of the item should increase dramatically
- Some items can have the "Damage" attribute. It can go from 0 to 10. The higher it is, the higher the price of the item
- Vehicle items shouldn't be valued too high.
- Items with category Accessory can be valued pretty high, but no more than $2000
- Items with category Skill Book should be valued higher than $100. For example, Vol.1 should be $500, then Vol.2 should be $1000, then Vol.3 should be $1500, and so on. This doesn't apply for magazines.
- Items with the same name but different FullType must be set with the same price but listed as separate
- Beaver related merch should cost higher than other items
- Random stuff shouldn't be valued too high, such as Vehicle Parts, Food utensils, Make Up, random tools, etc.
- Price can NEVER be 0. You can use at most 2 decimals though

This is the JSON of the previously generated prices, use them to keep new prices consistent: \n\n{old_prices}\n\n
Be concise and return a json with only the item FullType and its price. The item is: \n\n {new_prices}\n\n"""


with open('data/items.json') as json_file:
    data = json.load(json_file)



# Setup LLM
grammar_text = httpx.get("https://raw.githubusercontent.com/ggerganov/llama.cpp/master/grammars/json_arr.gbnf").text
grammar = LlamaGrammar.from_string(grammar_text) 
llm = LmmWorker(LmmEnum.Tess, grammar=grammar, n_ctx=1500, temperature=0.8)
llm.set_sys_message(SYSTEM_MESSAGE)


try:
    with open('output/dict_prices.json') as json_file:
        prices = json.load(json_file)
except FileNotFoundError:
    prices = []


starting_point = len(prices)

for i in tqdm.tqdm(range(starting_point, len(data), 1)):
    spliced_data = str(data[i:i+1])
    print(spliced_data)

    new_j = llm.run(prompt=BASE_PROMPT.format(new_prices=spliced_data, old_prices=prices[-25:]))    
    print(new_j)
    prices = [*prices, *new_j]

    with open('output/dict_prices.json', 'w') as file:
        file.write(json.dumps(prices, indent=4))

