from langchain_community.llms.llamacpp import LlamaCpp
from pydantic import ValidationError
import tqdm
import json
from gen_examples import setup_examples
from zomb_gen_common import OutputEnum, OutputJsonPrice,OutputJsonTag, get_data
from gen_prompt import get_suffix

from langchain.prompts import FewShotPromptTemplate
from langchain.chains import LLMChain


output_path = "output/prices.json"
model_path = "F:/models/llm/gguf/capybarahermes-2.5-mistral-7b.Q5_K_M.gguf"
t = OutputEnum.PRICE

#######################

output_type = OutputJsonPrice if t == OutputEnum.PRICE else OutputJsonTag

example_prompt, example_selector = setup_examples(t)
example_template = example_prompt.template
suffix = get_suffix(t)


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
    verbose=True,  # Verbose is required to pass to the callback manager
)

llm_chain = LLMChain( 
    prompt=similar_prompt,
    llm=llm,
    verbose=True,
)

data, prices = get_data(output_path)
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

        #try:
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
            raise ValueError("Generated more than one val")
        
        # Validate
        try:
            output_type.validate(new_j[0])
        except ValidationError:
            print("Data not valid")
            continue

        new_j[0]['fullType'] = fullType
        pbar.set_description(json.dumps(new_j), refresh=True)

        #print(new_j)

        prices = [*prices, *new_j]
        with open(output_path, 'w') as file:
            file.write(json.dumps(prices, indent=4))
        # except Exception:
        #     print("Failed execution, retrying")
        #     #print(new_j[0])
        #     continue


        # SAVE PREVIOUS DATA
        prev_input = spliced_data
        prev_output = result['text']

    i+=1
    pbar.update(1)

