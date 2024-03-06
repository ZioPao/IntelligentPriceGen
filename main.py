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

from examples import examples


BASE_PROMPT = """Based on the data I'm giving you try to guess a price and a tag.
    Price must be an integer.
    Choose one of the following tags: (WEAPON, AMMO, CLOTHING, MILITARY_CLOTHING, FOOD, FIRST_AID, VARIOUS, SKILL_BOOK, FURNITURE).

    Keep in mind the following rules when deciding the price:
    - Price can never be 0
    - Single bullets should cost less than ammo boxes

    The data to consider is the following:
    - FullType = {fullType}, 
    - Name = {name},
    - Weight = {weight},
    - Categories = {categories},
    - additionalData = {additionalData}

    Only for the given input data, answer with a JSON formatted as such: {{fullType: string, tag: string, price : integer}}. Don't add more than a single item inside the json.
"""

############################################################################################################

# Load data
with open('data/items.json') as json_file:
    data = json.load(json_file)

price_output = 'output/prices_test2.json'
try:
    with open(price_output, 'r') as json_file:
        prices = json.load(json_file)
except FileNotFoundError:
    prices = []

data = sorted(data, key=lambda d: d['fullType'])
prices = sorted(prices, key=lambda d: d['fullType'])






def run_generation(data, prices):
    
    ############################################################################################################

    model_path = "F:/models/llm/gguf/capybarahermes-2.5-mistral-7b.Q5_K_M.gguf"

    # Setup template


    example_template ="""
    Input:
    - FullType = {fullType}, 
    - Name = {name},
    - Weight = {weight},
    - Categories = {categories},
    - additionalData = {additionalData}

    Output:
    {output}
    """

    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    example_prompt = PromptTemplate(
        input_variables=["fullType", "name", "weight", "categories", "additionalData", "output"],
        template=example_template
    )


    # Setup embeddings
    embeddings = LlamaCppEmbeddings(model_path=model_path)

    to_vectorize = [" ".join(example.values()) for example in examples]
    vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=examples)

    example_selector = SemanticSimilarityExampleSelector(vectorstore=vectorstore, k=1)


    # Setup prompt

    prefix = """<|im_start|>system
    You're an obedient assistant. Always try to answer.
    Based on the data I'm giving you try to guess a price and a tag.
    Price must be an integer.
    Choose one of the following tags: (WEAPON, AMMO, CLOTHING, MILITARY_CLOTHING, FOOD, FIRST_AID, CAR_PARTS, VARIOUS, SKILL_BOOK, FURNITURE).

    Keep in mind the following rules when deciding the price:
    - Price can never be 0
    - Single bullets should cost less than ammo boxes<|im_end|>
    <|im_start|>user
    Return as the output ONLY data related to the following input and nothing more.
    Input:
    - FullType = {fullType}, 
    - Name = {name},
    - Weight = {weight},
    - Categories = {categories},
    - additionalData = {additionalData}

    
    Use the following data ONLY as an example:
    """


    similar_prompt = FewShotPromptTemplate(
        # We provide an ExampleSelector instead of examples.
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=prefix,
        suffix="""<|im_end|>
        <|im_start|>assistant
        Output:
        """,
        input_variables=["fullType", "name", "weight", "categories", "additionalData"],
    )



    llm = LlamaCpp(
        model_path=model_path,
        temperature=0.45,
        n_gpu_layers=-1,
        n_batch=1024,
        n_ctx=512,
    
        max_tokens=512,
        top_p=1,
        f16_kv=True,
        grammar_path ="json_grammar.gbnf", 
        callback_manager=callback_manager,
        verbose=False,  # Verbose is required to pass to the callback manager
        
    )
    llm_chain = LLMChain(prompt=similar_prompt, llm=llm)

    # Set up a parser + inject instructions into the prompt template.



    for i in tqdm.tqdm(range(0, len(data), 1)):
        spliced_data = data[i:i+1][0]       # with the examples as I made them it becomes VERY specific with the format that it wants.
        #print(spliced_data)
        fullType = spliced_data['fullType']
        name = spliced_data['name']
        weight = str(spliced_data['weight'])
        categories = spliced_data['category']
        additionalData = json.dumps(spliced_data['additionalData'])

        if additionalData != "None":
            additionalData = '{' + additionalData + '}'

        isFound = False
        for j in range(0, len(prices), 1):
            if fullType == prices[j]['fullType']:
                isFound = True
                break


        if not isFound:
            



            #spliced_data_as_str = json.dumps(spliced_data)

            print("Generating for " + fullType)

            print(similar_prompt.format(fullType=fullType, name=name, weight=weight, categories=categories, additionalData=additionalData))




            result = llm_chain.invoke({
                "fullType": fullType, "name": name, "weight": weight,
                "categories": categories, "additionalData": additionalData
                }
            )

            print(result['text'])



            #new_j = json.loads(result['text'])
            #print(new_j)
            #prices = [*prices, *new_j]

            # with open(price_output, 'w') as file:
            #     file.write(json.dumps(prices, indent=4))
            
            print("________________")



def check_generation(data, prices):
    for i in tqdm.tqdm(range(0, len(data), 1)):
        spliced_data = data[i:i+1][0]       # with the examples as I made them it becomes VERY specific with the format that it wants.
        #print(spliced_data)
        fullType = spliced_data['fullType']

        isFound = False
        for j in range(0, len(prices), 1):
            if fullType == prices[j]['fullType']:
                isFound = True
                break

        if not isFound:
            print(fullType + " NOT FOUND!!!!!!!!!!!!!!!!!")



#check_generation(data=data, prices=prices)
run_generation(data=data, prices=prices)
# https://medium.com/@yernenip/few-shot-prompting-with-codellama-langchain-and-mysql-94020ee16a08


