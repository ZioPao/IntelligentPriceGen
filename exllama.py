#model_directory = "F:\models\llm\exl2\TinyLlama-1B-32k-exl2"
model_directory = "F:\models\llm\exl2\OpenHermes-2.5-Code-290k-13B-8.0bpw-h8-exl2"



import json
from exllamav2 import(
    ExLlamaV2,
    ExLlamaV2Config,
    ExLlamaV2Cache,
    ExLlamaV2Tokenizer,
)

from exllamav2.generator import (
    ExLlamaV2BaseGenerator,
    ExLlamaV2Sampler
)

# Initialize model and cache

config = ExLlamaV2Config()
config.model_dir = model_directory
config.prepare()

model = ExLlamaV2(config)
print("Loading model: " + model_directory)

cache = ExLlamaV2Cache(model, lazy = True)
model.load_autosplit(cache)

tokenizer = ExLlamaV2Tokenizer(config)

# Initialize generator

generator = ExLlamaV2BaseGenerator(model, cache, tokenizer)

# Prepare settings

settings = ExLlamaV2Sampler.Settings()
settings.temperature = 0.85
settings.top_k = 50
settings.top_p = 0.8
settings.disallow_tokens(tokenizer, [tokenizer.eos_token_id])

max_new_tokens = 150

generator.warmup()



#########################

from lmformatenforcer.characterlevelparser import CharacterLevelParser
from lmformatenforcer.integrations.exllamav2 import ExLlamaV2TokenEnforcerFilter
from typing import Optional

def exllamav2_with_format_enforcer(prompt: str, parser: Optional[CharacterLevelParser] = None) -> str:
    if parser is None:
        settings.filters = []
    else:
        settings.filters = [ExLlamaV2TokenEnforcerFilter(parser, tokenizer)]
    result = generator.generate_simple(prompt, settings, max_new_tokens, seed = 1234)

    stripped_r = result[len(prompt):]
    stripped_r = stripped_r.replace("⁇", "")        # no idea where this is coming from
    #stripped_r = stripped_r.lstrip()

    return json.loads(stripped_r)


from lmformatenforcer import JsonSchemaParser
from pydantic import BaseModel



def display_header(text):
    print(text)

def display_content(text):
    print(text)

class AnswerFormat(BaseModel):
    fullType: str
    price: int
    tag : str

BASE_PROMPT = """Consider this JSON: {new_prices}\n\n

I'm creating an economy system in a game.
I'll give you the following data in json form:
- Item Name
- Item FullType (You can understand better what it is)
- Item Weight
- Item Categories (Could be empty)
- Item BulletDefense Stat (Could be empty)
- Item Damage Stat (Could be empty)

Keep in mind:
- Weapons must be valued pretty high (AT LEAST $2500), but generally (especially for guns) you can go much higher. Account for other attributes, such as its weight and damage.\n
- Single bullets should cost a FRACTION of a clip or ammo boxex, like $1 or $2 per single bullet. These items must be set with the tag AMMO.
- Military items and military clothing items must be valued pretty high (AT LEAST $2000). Use their attributes, such as bullet defense, to guess an estimate.\n
- Items listed with Category "Blunt" are weapons.\n
- Some items can have the "BulletDefense" attribute. If it's higher than 0, the cost of the item should increase dramatically.\n
- Some items can have the "Damage" attribute. It can go from 0 to 10. The higher it is, the higher the price of the item.\n
- Items related to vehicles, like Trunks, shouldn't be valued too high and can be considered JUNK
- Items with category Accessory can be valued pretty high, but no more than $2000.\n
- Items with category Skill Book should be valued higher than $100. For example, Vol.1 should be $500, then Vol.2 should be $1000, then Vol.3 should be $1500, and so on. This doesn't apply for magazines.\n
- Items with the same name but different FullType must be set with the same price but listed as separate.\n
- Items that start with BBB in their fulltype should be valued WAY higher than other items.\n
- Items that start with Mov_ in their fullType are furniture, and should cost a lot\n
- Random stuff shouldn't be valued too high, such as Vehicle Parts, Food utensils, Make Up, random tools, etc. You can go as low as $5\n
- Price can NEVER be 0. You can use at most 2 decimals though.\n\n

Choose between the following TAGS depending on the item name and category:
- WEAPON
- AMMO
- CLOTHING
- MILITARY_CLOTHING
- FOOD
- FIRST_AID
- VARIOUS
- SKILL_BOOK
- FURNITURE

Use ONLY the tags that have been specified here.

This is the JSON of the previously generated prices, use them to keep new prices/tags consistent: \n\n{old_prices}\n\n
You MUST answer using the following json schema:
"""

question_with_schema = f'{BASE_PROMPT}{AnswerFormat.schema_json()}'
prompt = question_with_schema



import tqdm
parser = JsonSchemaParser(AnswerFormat.schema())


with open('data/items.json') as json_file:
    data = json.load(json_file)


price_output = 'output/prices_' + "exllama" + '.json'

try:
    with open(price_output, 'r') as json_file:
        prices = json.load(json_file)
except FileNotFoundError:
    prices = []



# Order data
#data = sorted(data, key=lambda d: d['fullType'])
#prices = sorted(prices, key=lambda d: d['fullType'])

#starting_point = len(prices)

amount_of_data = 1

for i in tqdm.tqdm(range(0, len(data), amount_of_data)):

    fType = data[i:i+1][0]['fullType']
    spliced_data = str(data[i:i+amount_of_data])
    #print()

    #print(prices[i]['fullType'])
    #ugly time, the json struct is pretty awful

    isFound = False
    # for j in range(0, len(prices), 1):
    #     if fType == prices[j]['fullType']:
    #         isFound = True
    #         break

    if not isFound:
        #print(fType)
        new_p = f'{BASE_PROMPT.format(new_prices=spliced_data, old_prices=prices[-10:])}{AnswerFormat.schema_json()}'

        new_j = exllamav2_with_format_enforcer(prompt=new_p, parser=parser)    
        print(new_j)
        prices = [*prices, *new_j]

        with open(price_output, 'w') as file:
            file.write(json.dumps(prices, indent=4))

        print("_____________________________\n\n")
