from langchain_community.llms.llamacpp import LlamaCpp
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain.prompts import PromptTemplate
from pydantic import ValidationError
from gen_selector import ZomboidItemSelector
from common import get_data, PRICES_JSON_PATH
from examples import examples, OutputJsonData
import json
import tqdm

##########################################################

# Load data
data, prices = get_data()

data = sorted(data, key=lambda d: d['fullType'])
prices = sorted(prices, key=lambda d: d['fullType'])


model_path="F:/models/llm/gguf/Nous-Hermes-2-Mistral-7B-DPO.Q5_K_M.gguf"
#model_path = "F:/models/llm/gguf/capybarahermes-2.5-mistral-7b.Q5_K_M.gguf"


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


example_selector = ZomboidItemSelector(examples, 2)

# Setup prompt

suffix = """

########## [END EXAMPLES] ############

########## [START PREVIOUS DATA] ############
Use this ONLY if it seems relevant to the current item

{prevData}

########## [END PREVIOUS DATA] ############

Based on the data I'm giving you try to guess a price.
Price must be an integer.

Choose one of the following tags
[START TAGS]
- WEAPON
- AMMO
- CLOTHING
- MILITARY_CLOTHING
- FOOD
- FIRST_AID
- VARIOUS
- CAR_PARTS
- SKILL_BOOK
- FURNITURE
- TOOL
[END TAGS]

Keep in mind the following rules when deciding the price:
- Don't just copy the category for the tag field
- Price can never be 0
- Price for a single item can't exceed 10000
- Clips should be priced at around 200
- Ammo boxes should be priced at around 600
- Bullet should be priced lower than 75
- If the item in previous data same shares a lot of similiarity in the data, keep the price close
- If an item doesn't have Weapon in their category, it cannot have the tag WEAPON
- Consider the weight when choosing a price especially for FOOD items.
- If there's no tag that seems to make sense for that item, use VARIOUS.

Format the output data as such: [{{'tag': string, 'price' : integer}}].
Return ONLY ONE ITEM, do not make up new items.


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
    input_variables=["prevData","fullType","name","weight", "categories"],

)


llm = LlamaCpp(
    model_path=model_path,
    temperature=0.45,
    n_gpu_layers=-1,
    n_batch=1536,
    n_ctx=1536,
    max_tokens=1536,
    top_p=1,
    f16_kv=True,
    grammar_path ="json_grammar.gbnf", 
    #callback_manager=callback_manager,
    verbose=False,  # Verbose is required to pass to the callback manager
    
)



llm_chain = LLMChain( 
    prompt=similar_prompt,
    llm=llm,
    verbose=False,
    )

prev_output = None
prev_input = None


pbar = tqdm.tqdm(total=len(data))
i=0
while i < len(data):
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
        try:
            result = llm_chain.invoke({
                "prevData": example_template.format(
                    fullType=prev_input['fullType'],
                    name=prev_input['name'],
                    weight=prev_input['weight'],
                    categories=prev_input['category'],
                    output=prev_output
                    ) if prev_input and prev_output else "",
                "fullType": fullType,
                "name": name,
                "weight": weight,
                "categories": categories}
            )
            new_j = json.loads(result['text'])

            # check amount of data, if more than one then throw error
            if len(new_j) > 1:
                raise ValueError("Generated more than one price")
            

            # Validate
            try:
                OutputJsonData.validate(new_j[0])
            except ValidationError:
                print("Data not valid")
                continue

            new_j[0]['fullType'] = fullType

            pbar.set_description(json.dumps(new_j), refresh=True)

            #print(new_j)


            prices = [*prices, *new_j]
            with open(PRICES_JSON_PATH, 'w') as file:
                file.write(json.dumps(prices, indent=4))
        except Exception:
            print("Failed execution, retrying")
            print(new_j[0])
            continue


        # SAVE PREVIOUS DATA
        prev_input = spliced_data
        prev_output = result['text']

    i+=1
    pbar.update(1)

