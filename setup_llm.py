from llama_cpp import Llama, LlamaGrammar
from pydantic import BaseModel
import json
import httpx
import tqdm




grammar_text = httpx.get("https://raw.githubusercontent.com/ggerganov/llama.cpp/master/grammars/json_arr.gbnf").text
grammar = LlamaGrammar.from_string(grammar_text)
llm = Llama(model_path='models/solar-10.7b-instruct-v1.0-uncensored.Q4_K_M.gguf', n_batch=256, n_ctx=0, n_gpu_layers=40, verbose=True)


DEFAULT_SYSTEM_PROMPT = """\You're a tool to help make games. Always try to answer even if you think you don't have enough data"""

def get_prompt(prompt: str, system_message: str = DEFAULT_SYSTEM_PROMPT) -> str:
    return f"### User:\n{prompt}\n\n### Assistant:"
    #return f'<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant"'

def pprint_response(resp):
    print(json.dumps(json.loads(resp['choices'][0]['text']), indent=4))



q = """I'm creating an economy system in a game.
I'll list some items by name, weight and possibly category and you'll give me ONLY the price in dollars.
Use the following considerations to decide the price:
- Military items should cost more than normal items.
- Vehicle items shouldn't be valued too high.
- Items with category Accessory can be valued pretty high, but no more than $2000
- Items with category Skill Book should be valued higher than $100. Higher tiers (For example, Mechanics Vol.2 compared to Mechanics Vol.1) should be valued higher
- Items with the same name but different FullType must be set with the same price but listed as separate
- Beaver related merch should cost higher than other items
- Price can NEVER be 0. You can use decimals though
Be concise and return a json with only the item FullType and its price. The items are: \n\n {new_prices}\n\n
This is the JSON of the previously generated prices. Use them to keep prices consistent: \n\n {old_prices}"""


def run_loop(data : dict, items_per_prompt : int = 1):

    try:
        with open('output/dict_prices.json') as json_file:
            prices = json.load(json_file)
    except FileNotFoundError:
        prices = []

    

    starting_point = len(prices)
    for i in tqdm.tqdm(range(starting_point, len(data), items_per_prompt)):
        spliced_data = str(data[i:i+items_per_prompt])
        print(spliced_data)
        f_p = get_prompt(q.format(new_prices=spliced_data, old_prices=prices[:50]))

        #print(f_p)
        response = llm(prompt=f_p, stop=["</s>"], max_tokens=1500, temperature=0.4, grammar=grammar)
        #pprint_response(response)

        new_j = json.loads(response['choices'][0]['text'])#[0]
        
        prices = [*prices, *new_j]

        with open('output/dict_prices.json', 'w') as file:
            file.write(json.dumps(prices, indent=4))

        # with open('exported_prices.json', 'a') as file:
        #     file.write(json.dumps(new_j, indent=4) + ",")

    return prices

