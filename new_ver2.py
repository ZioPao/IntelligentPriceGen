from langchain_community.embeddings import LlamaCppEmbeddings
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain_community.vectorstores import Chroma
from langchain.chains import LLMChain
from langchain_community.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
import json

import tqdm

from pydantic import BaseModel, Field
from typing import Deque, List, Optional, Tuple

class InputJsonData(BaseModel):

    fullType: str
    name: str
    category: str = "[]"
    weight: float
    additionalData: Optional[str] = "{{}}" 


    def model_dump_json(self, *, indent: int | None = None, include: set[int] | set[str] | dict[int, any] | dict[str, any] | None = None, exclude: set[int] | set[str] | dict[int, any] | dict[str, any] | None = None, by_alias: bool = False, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, round_trip: bool = False, warnings: bool = True) -> str:
        return "{" + super().model_dump_json(indent=indent, include=include, exclude=exclude, by_alias=by_alias, exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none, round_trip=round_trip, warnings=warnings) + "}"



class OutputJsonData(BaseModel):
    fullType: str
    price: int
    tag : str

    def model_dump_json(self, *, indent: int | None = None, include: set[int] | set[str] | dict[int, any] | dict[str, any] | None = None, exclude: set[int] | set[str] | dict[int, any] | dict[str, any] | None = None, by_alias: bool = False, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, round_trip: bool = False, warnings: bool = True) -> str:
        return "{" + super().model_dump_json(indent=indent, include=include, exclude=exclude, by_alias=by_alias, exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none, round_trip=round_trip, warnings=warnings) + "}"



examples = [


    # Essential Items as a base
    {
        "input": InputJsonData(fullType="Base.GranolaBar", name="Granola Bar", category="[Food]", weight=0.2).model_dump_json(),
        "output": OutputJsonData(fullType="Base.GranolaBar", price=20, tag="FOOD").model_dump_json()
    },
    {
        "input": InputJsonData(fullType="Base.BaseballBat", name="Baseball Bat", weight=2, category="[Blunt, Sports]", additionalData=r'{"damage": 0.95}').model_dump_json(),
        "output": OutputJsonData(fullType="Base.BaseballBat", price=200, tag="WEAPON").model_dump_json()
    },
    {
        "input": InputJsonData(fullType="Base.ShotgunSawnoff", name="Sawed-Off Double Barrel Shotgun", weight=3, category="[Weapon]", additionalData=r'{"damage": 2.35}').model_dump_json(),
        "output": OutputJsonData(fullType="Base.ShotgunSawnoff", price=1500, tag="WEAPON").model_dump_json()
    },
    {
        "input": InputJsonData(fullType="Base.Bullets9mmBox", name="Box of 9mm Rounds", weight=0.2, category="[Ammo]").model_dump_json(),
        "output": OutputJsonData(fullType="Base.Bullets9mmBox", price=250, tag="AMMO").model_dump_json()
    },
    {
        "input": InputJsonData(fullType="Base.Bullets9mm", name="9mm Round", weight=0.0099999997764826, category="[Ammo]").model_dump_json(),
        "output": OutputJsonData(fullType="Base.Bullets9mm", price=9, tag="AMMO").model_dump_json()
    },


    # Random Junk
    {
        "input": InputJsonData(fullType="Base.ToiletPaper", name="Toilet Paper", weight=0.2, category="[Junk]").model_dump_json(), 
        "output": OutputJsonData(fullType="Base.ToiletPaper", price=5, tag="VARIOUS").model_dump_json()
    },
    


    # Beaver example
    # - Items with FullType that starts with BBB. should have a price of at least 2000
    {
        "input": InputJsonData(fullType="BBB.Tshirt_BBB_SittingBeaver", name="Sitting Beaver T-Shirt", weight=1, category="[Clothing]").model_dump_json(), 
        "output": OutputJsonData(fullType="BBB.Tshirt_BBB_SittingBeaver", price=2500, tag="CLOTHING").model_dump_json()
    },


]


############################################################################################################

# Load data
with open('data/items.json') as json_file:
    data = json.load(json_file)

price_output = 'output/prices_test.json'
try:
    with open(price_output, 'r') as json_file:
        prices = json.load(json_file)
except FileNotFoundError:
    prices = []

data = sorted(data, key=lambda d: d['fullType'])
prices = sorted(prices, key=lambda d: d['fullType'])







############################################################################################################

model_path = "F:/models/llm/gguf/capybarahermes-2.5-mistral-7b.Q5_K_M.gguf"

# Setup template

template="""<|im_start|>system
You're an obedient assistant. Always try to answer.<|im_end|>
<|im_start|>user
{input}<|im_end|>
<|im_start|>assistant{output}"""

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template=template
)


# Setup embeddings
embeddings = LlamaCppEmbeddings(model_path=model_path)
example_selector = SemanticSimilarityExampleSelector.from_examples(
    # The list of examples available to select from.
    examples,
    # The embedding class used to produce embeddings which are used to measure semantic similarity.
    embeddings,
    # The VectorStore class that is used to store the embeddings and do a similarity search over.
    Chroma,
    # The number of examples to produce.
    k=1,
)


# Setup prompt

prefix = """Based on the in input JSON, try to guess a price and a tag.
Price must be an integer.
Choose one of the following tags: (WEAPON, AMMO, CLOTHING, MILITARY_CLOTHING, FOOD, FIRST_AID, VARIOUS, SKILL_BOOK, FURNITURE).

Keep in mind the following rules when deciding the price:
- Price can never be 0
- Single bullets should cost less than ammo boxes

Return the result in a json formatted like this: [{{fullType: string, tag: string, price : integer}}]"""


similar_prompt = FewShotPromptTemplate(
    # We provide an ExampleSelector instead of examples.
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix=prefix,
    suffix="Input: {input}\nOutput:",
    input_variables=["input"],
)



llm = LlamaCpp(
    model_path=model_path,
    temperature=0.75,
    n_gpu_layers=-1,
    n_batch=2000,
    max_tokens=2000,
    top_p=1,
    f16_kv=True,
    callback_manager=callback_manager,
    verbose=True,  # Verbose is required to pass to the callback manager
    
)
llm_chain = LLMChain(prompt=similar_prompt, llm=llm)

for i in tqdm.tqdm(range(0, len(data), 1)):
    spliced_data = str(data[i:i+1][0])
    print(spliced_data)
    result = llm_chain.invoke({"input":spliced_data})
    print("________________")




# https://medium.com/@yernenip/few-shot-prompting-with-codellama-langchain-and-mysql-94020ee16a08












# # Examples of a pretend task of creating antonyms.
# examples = [

#     ## EXAMPLE DATA


#     {"input": '{{"fullType":"Base.ToiletPaper","name":"Toilet Paper","category":"[Junk]","weight":0.20000000298023,"additionalData":"{{}}" }}',
#      "output": '[{{"fullType": "Base.ToiletPaper","price": 5, "tag": "VARIOUS"}}]'},


    

#     ## WEAPONS

#     {"input", '{{"fullType":"Base.9mmClip","name":"M9 Magazine","category":"[Ammo]","weight":0.10000000149012,"additionalData":"{{}}" }}',
#      "output": '[{{"fullType: "Base.9mmClip", "price": }}]'}


# ]


# 


# example_selector = SemanticSimilarityExampleSelector.from_examples(
#     # The list of examples available to select from.
#     examples,
#     # The embedding class used to produce embeddings which are used to measure semantic similarity.
#     embeddings,
#     # The VectorStore class that is used to store the embeddings and do a similarity search over.
#     Chroma,
#     # The number of examples to produce.
#     k=1,
# )


# prefix = """Based on the in input JSON, try to guess a price and a tag.
# Price must be an integer.
# Choose one of the following tags: (WEAPON, AMMO, CLOTHING, MILITARY_CLOTHING, FOOD, FIRST_AID, VARIOUS, SKILL_BOOK, FURNITURE).

# Keep in mind the following rules when deciding the price:
# - Price can never be 0
# - Single bullets should cost less than ammo boxes
# - Items with FullType that starts with BBB. should have a price of at least 2000

# Return the result in a json formatted like this: [{{fullType: string, tag: string, price : integer}}]"""


# similar_prompt = FewShotPromptTemplate(
#     # We provide an ExampleSelector instead of examples.
#     example_selector=example_selector,
#     example_prompt=example_prompt,
#     prefix=prefix,
#     suffix="Input: {json_data}\nOutput:",
#     input_variables=["json_data"],
# )


# example_data = '{{"fullType":"MoreTraits.AntiqueSpear","name":"Antique Spear","category":"[Improvised, Spear, WeaponCrafted]","weight":2,"additionalData":{"damage":1.75}}}'

# # Input is a feeling, so should select the happy/sad example
# llm = LlamaCpp(
#     model_path="F:/models/llm/gguf/capybarahermes-2.5-mistral-7b.Q5_K_M.gguf",
#     temperature=0.75,
#     n_gpu_layers=-1,
#     n_batch=2000,
#     max_tokens=2000,
#     top_p=1,
#     f16_kv=True,
#     callback_manager=callback_manager,
#     verbose=True,  # Verbose is required to pass to the callback manager
    
# )

# llm_chain = LLMChain(prompt=similar_prompt, llm=llm)

# result = llm_chain.invoke({"json_data":example_data})




# with open('data/items.json') as json_file:
#     data = json.load(json_file)

# price_output = 'output/prices_test.json'
# try:
#     with open(price_output, 'r') as json_file:
#         prices = json.load(json_file)
# except FileNotFoundError:
#     prices = []

# ###  Generate examples first

# import tqdm
# for i in tqdm.tqdm(range(0, len(data), 1)):

#     fType = data[i:i+1][0]['fullType']
#     spliced_data = str(data[i:i+1])