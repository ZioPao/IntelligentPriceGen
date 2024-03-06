from langchain_community.embeddings import LlamaCppEmbeddings
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector, NGramOverlapExampleSelector, MaxMarginalRelevanceExampleSelector
from langchain_community.vectorstores import Chroma
from langchain.chains import LLMChain
from langchain_community.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json

import tqdm

from pydantic import BaseModel, Field
from typing import Deque, List, Optional, Tuple


from examples import examples, OutputJsonData
from gen_selector import FullTypeSelector


##########################################################

# Load data
with open('data/items.json') as json_file:
    data = json.load(json_file)

price_output = 'output/prices_test_new.json'
try:
    with open(price_output, 'r') as json_file:
        prices = json.load(json_file)
except FileNotFoundError:
    prices = []

data = sorted(data, key=lambda d: d['fullType'])
prices = sorted(prices, key=lambda d: d['fullType'])



model_path = "F:/models/llm/gguf/capybarahermes-2.5-mistral-7b.Q5_K_M.gguf"
example_template ="""
Input:
- FullType = {fullType}, 
- Name = {name},
- Weight = {weight},
- Categories = {categories},

Output:
{output}
"""


callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

example_prompt = PromptTemplate(
    input_variables=["fullType", "name", "weight", "categories", "output"],
    template=example_template
)

# Setup embeddings
embeddings = LlamaCppEmbeddings(model_path=model_path)

# to_vectorize = [" ".join(example.values()) for example in examples]
# vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=examples)

# example_selector = SemanticSimilarityExampleSelector(vectorstore=vectorstore, k=4)


example_selector = FullTypeSelector(examples)

# Setup prompt

suffix = """
########## [END EXAMPLES] ############

Based on the data I'm giving you try to guess a price and a tag.
Price must be an integer.
Choose one of the following tags: (WEAPON, AMMO, CLOTHING, MILITARY_CLOTHING, FOOD, FIRST_AID, VARIOUS, SKILL_BOOK, FURNITURE).

Keep in mind the following rules when deciding the price:
- Price can never be 0
- Single bullets should cost less than ammo boxes

Format the output data as such: [{{fullType: string, tag: string, price : integer}}]


############ [START INPUT DATA] ###############

- FullType = {fullType}, 
- Name = {name},
- Weight = {weight},
- Categories = {categories},

############ [END INPUT DATA] ###############

"""



similar_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_separator="",
    example_prompt=example_prompt,
    prefix="############ [START EXAMPLES] ############'\n",
    suffix=suffix,
    input_variables=["fullType", "name", "weight", "categories"],

)


llm = LlamaCpp(
    model_path=model_path,
    temperature=0.75,
    n_gpu_layers=-1,
    n_batch=2000,
    n_ctx=1536,

    max_tokens=2000,
    top_p=1,
    f16_kv=True,
    grammar_path ="json_grammar.gbnf", 
    callback_manager=callback_manager,
    verbose=True,  # Verbose is required to pass to the callback manager
    
)

# Set up a parser + inject instructions into the prompt template.
parser = JsonOutputParser(pydantic_object=OutputJsonData)



llm_chain = LLMChain(
    prompt=similar_prompt,
    llm=llm,
    verbose=True,
    )



for i in tqdm.tqdm(range(0, len(data), 1)):
    spliced_data = data[i:i+1][0]       # with the examples as I made them it becomes VERY specific with the format that it wants.
    fullType = spliced_data['fullType']
    name = spliced_data['name']
    weight = str(spliced_data['weight'])
    categories = spliced_data['category']

    isFound = False
    for j in range(0, len(prices), 1):
        if fullType == prices[j]['fullType']:
            isFound = True
            break

    if not isFound:
        result = llm_chain.invoke({
            "fullType": fullType,
            "name": name,
            "weight": weight,
            "categories": categories}
        )
        new_j = json.loads(result['text'])
        prices = [*prices, *new_j]
        with open(price_output, 'w') as file:
            file.write(json.dumps(prices, indent=4))


    new_j = json.loads(result['text'])
    print(new_j)
    print("________________")

