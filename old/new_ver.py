import json
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp
from langchain.embeddings import LlamaCppEmbeddings
import tqdm

# IMPORT AND SORT DATA


# TODO Add examples


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
######################################

system_msg = "You are an obedient assistant. Always try to answer"

template = """<|im_start|>system
{system_message}<|im_end|>
<|im_start|>user
{question}<|im_end|>
<|im_start|>assistant"""

prompt = PromptTemplate.from_template(template)

# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

llm = LlamaCpp(
    model_path="F:/models/llm/gguf/capybarahermes-2.5-mistral-7b.Q5_K_M.gguf",
    temperature=0.75,
    n_gpu_layers=-1,
    n_batch=2000,
    max_tokens=2000,
    top_p=1,
    f16_kv=True,
    callback_manager=callback_manager,
    verbose=True,  # Verbose is required to pass to the callback manager
    grammar_path ="json_grammar.gbnf"
)

llm_chain = LLMChain(prompt=prompt, llm=llm)

question = """Based on this Json: {json_data}, try to guess a price and a tag.
Price must be an integer.
Choose one of the following tags: (WEAPON, AMMO, CLOTHING, MILITARY_CLOTHING, FOOD, FIRST_AID, VARIOUS, SKILL_BOOK, FURNITURE).

Keep in mind the following rules when deciding the price:
- Price can never be 0
- Single bullets should cost less than ammo boxes
- Items with FullType that starts with BBB. should have a price of at least 2000

Use this old generated data as a reference for future generations: {old_generated_data}.

Return the result in a json formatted like this: [{{fullType: string, tag: string, price : integer}}]"""

amount_of_data = 1



for i in tqdm.tqdm(range(0, len(data), amount_of_data)):

    fType = data[i:i+1][0]['fullType']
    spliced_data = str(data[i:i+amount_of_data])
    #print()

    #print(prices[i]['fullType'])
    #ugly time, the json struct is pretty awful

    isFound = False
    for j in range(0, len(prices), 1):
        if fType == prices[j]['fullType']:
            print("Found " + fType + " in generated prices")
            isFound = True
            break

    if not isFound:
        #print(fType)
        try:
            formatted_question = question.format(json_data=spliced_data, old_generated_data=prices[-5:])

            result = llm_chain.invoke({"system_message" : system_msg, "question": formatted_question})
            new_j = json.loads(result['text'])
            
            prices = [*prices, *new_j]

            with open(price_output, 'w') as file:
                file.write(json.dumps(prices, indent=4))
        except Exception:
            i=i-amount_of_data
            continue

        print("_____________________________\n\n")


