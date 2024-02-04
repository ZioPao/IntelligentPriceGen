from llama_cpp import Llama, LlamaGrammar
from pydantic import BaseModel
import json
import httpx
import tqdm


DEFAULT_SYSTEM_PROMPT = """\You're a tool to help make games. Always try to answer even if you think you don't have enough data"""

def get_prompt(prompt: str, system_message: str = DEFAULT_SYSTEM_PROMPT) -> str:
    return f'<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant"'

def pprint_response(resp):
    print(json.dumps(json.loads(resp['choices'][0]['text']), indent=4))

grammar_text = httpx.get("https://raw.githubusercontent.com/ggerganov/llama.cpp/master/grammars/json_arr.gbnf").text
grammar = LlamaGrammar.from_string(grammar_text)
llm = Llama(model_path='models/capybarahermes-2.5-mistral-7b.Q5_K_M.gguf', n_batch=512, n_ctx=0, n_gpu_layers=50, verbose=True)

q = """I'm creating an economy system in a game.
I'll list some items by name, weight and possibly category and you'll give me ONLY the price in dollars.
Use the following considerations to decide the price:
- Military items should cost more than normal items.
- Vehicle items shouldn't be valued too high.
- Items with category Accessory can be valued pretty high, but no more than $2000
- Items with category Skill Book should be valued higher than $100
- Items with the same name but different FullType must be set with the same price but listed as separate
- Beaver related merch should cost higher than other items
- Price can NEVER be 0. You can use decimals though
Be concise and return a json with only the item FullType and its price. The items are: \n\n"""


def run_loop(data : dict, items_per_prompt : int):

    dict_prices = []

    for i in tqdm.tqdm(range(0, len(data), items_per_prompt)):
        spliced_data = str(data[i:i+items_per_prompt])
        f_p = get_prompt(q + spliced_data)

        print(f_p)
        response = llm(prompt=f_p, stop=["</s>"], max_tokens=-1, temperature=0.4, grammar=grammar)
        pprint_response(response)

        new_j = json.loads(response['choices'][0]['text'])#[0]
        
        dict_prices = [*dict_prices, *new_j]

        with open('temp_dict_prices.json', 'w') as file:
            file.write(json.dumps(dict_prices, indent=4))

        # with open('exported_prices.json', 'a') as file:
        #     file.write(json.dumps(new_j, indent=4) + ",")

    return dict_prices

