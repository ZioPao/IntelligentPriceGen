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






def run_generation(data, prices):
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


        # Skill books

        {
            "input": InputJsonData(fullType="Base.BookBlacksmith1", name="Blacksmith Vol. 1", weight=0.8, category="[SkillBook]").model_dump_json(),
            "output": OutputJsonData(fullType="Base.BookBlacksmith1", price=150, tag="SKILL_BOOK").model_dump_json()
        },
        {
            "input": InputJsonData(fullType="Base.BookBlacksmith2", name="Blacksmith Vol. 2", weight=0.8, category="[SkillBook]").model_dump_json(),
            "output": OutputJsonData(fullType="Base.BookBlacksmith2", price=300, tag="SKILL_BOOK").model_dump_json()
        },
        {
            "input": InputJsonData(fullType="Base.BookBlacksmith3", name="Blacksmith Vol. 3", weight=0.8, category="[SkillBook]").model_dump_json(),
            "output": OutputJsonData(fullType="Base.BookBlacksmith3", price=600, tag="SKILL_BOOK").model_dump_json()
        },
        {
            "input": InputJsonData(fullType="Base.BookBlacksmith4", name="Blacksmith Vol. 4", weight=0.8, category="[SkillBook]").model_dump_json(),
            "output": OutputJsonData(fullType="Base.BookBlacksmith4", price=1200, tag="SKILL_BOOK").model_dump_json()
        },    {
            "input": InputJsonData(fullType="Base.BookBlacksmith5", name="Blacksmith Vol. 5", weight=0.8, category="[SkillBook]").model_dump_json(),
            "output": OutputJsonData(fullType="Base.BookBlacksmith5", price=2400, tag="SKILL_BOOK").model_dump_json()
        },


        # Bags as clothing

        {
            "input": InputJsonData(fullType="Base.Bag_DuffelBagTINT", name="Duffel Bag", weight=1, category="[Bag]").model_dump_json(),
            "output": OutputJsonData(fullType="Base.Bag_DuffelBagTINT", price=500, tag="CLOTHING").model_dump_json()
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

    model_path = "F:/models/llm/gguf/capybarahermes-2.5-mistral-7b.Q5_K_M.gguf"

    # Setup template


    example_template ="""
    Input: {input}
    Output: {output}
    """

    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    example_prompt = PromptTemplate(
        input_variables=["input", "output"],
        template=example_template
    )


    # Setup embeddings
    embeddings = LlamaCppEmbeddings(model_path=model_path)

    to_vectorize = [" ".join(example.values()) for example in examples]
    vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=examples)

    example_selector = SemanticSimilarityExampleSelector(vectorstore=vectorstore, k=1)


    # Setup prompt

    prefix = """<|im_start|>system
    You're an obedient assistant. Always try to answer.<|im_end|>
    <|im_start|>user
    Based on the data I'm giving you try to guess a price and a tag.
    Price must be an integer.
    Choose one of the following tags: (WEAPON, AMMO, CLOTHING, MILITARY_CLOTHING, FOOD, FIRST_AID, VARIOUS, SKILL_BOOK, FURNITURE).

    Keep in mind the following rules when deciding the price:
    - Price can never be 0
    - Single bullets should cost less than ammo boxes

    The data to consider is: {input}
    Only for the given input data, answer with a JSON formatted as such: [{{fullType: string, tag: string, price : integer}}]. Don't add more than a single item inside the json.<|im_end|>
    """


    similar_prompt = FewShotPromptTemplate(
        # We provide an ExampleSelector instead of examples.
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=prefix,
        suffix="""<|im_start|>assistant""",
        input_variables=["input"],
    )



    llm = LlamaCpp(
        model_path=model_path,
        temperature=0.55,
        n_gpu_layers=-1,
        n_batch=2000,
        max_tokens=2000,
        top_p=1,
        f16_kv=True,
        grammar_path ="json_grammar.gbnf", 
        callback_manager=callback_manager,
        verbose=True,  # Verbose is required to pass to the callback manager
        
    )
    llm_chain = LLMChain(prompt=similar_prompt, llm=llm)


    for i in tqdm.tqdm(range(0, len(data), 1)):
        spliced_data = data[i:i+1][0]       # with the examples as I made them it becomes VERY specific with the format that it wants.
        #print(spliced_data)
        fType = spliced_data['fullType']

        isFound = False
        for j in range(0, len(prices), 1):
            if fType == prices[j]['fullType']:
                isFound = True
                break


        if not isFound:
            print(fType)
            spliced_data_as_str = json.dumps(spliced_data)
            result = llm_chain.invoke({"input":spliced_data_as_str})

            new_j = json.loads(result['text'])
            prices = [*prices, *new_j]

            with open(price_output, 'w') as file:
                file.write(json.dumps(prices, indent=4))
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



check_generation(data=data, prices=prices)
#run_generation(data=data, prices=prices)
# https://medium.com/@yernenip/few-shot-prompting-with-codellama-langchain-and-mysql-94020ee16a08


