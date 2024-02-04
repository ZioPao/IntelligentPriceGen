from llama_cpp import Llama
import re



def return_item_names():
    item_names = []
    with open('new_items.txt', 'r') as file:
        for line in file:
            pairs = line.strip().split(", ")
            if pairs:
                try:
                    item_name = pairs[2]
                except IndexError:
                    item_name = None

                if item_name:
                    item_names.append(re.match("displayName: (.*)", item_name)[1])
    return item_names


def execute_llm(llm, prompt):
    z = llm.create_chat_completion(
            messages = [
                {"role": "system", 
                "content": "I'm building an economy in a game. I will provide you with the name of a single item and you must give me its price in dollars. I will provide you with a list of items. Your answer will be formatted like NAME OF THE ITEM: $PRICE"},
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
    print(z['choices'][0]['message']['content'])







llm = Llama(model_path='models/capybarahermes-2.5-mistral-7b.Q5_K_M.gguf', chat_format='llama-2', n_gpu_layers=-1, n_batch=521, verbose=False)

names = return_item_names()

prompt = ""
counter = 0
for x in names:
    counter += 1

    prompt += x
    if counter > 10:
        execute_llm(llm, prompt)
        prompt = ""
        counter = 0
    else:
        prompt += ", "















# prompt = ""

# counter = 0
# with open('new_items.txt', 'r') as file:
#     for line in file:
#         pairs = line.strip().split(", ")
        
#         if pairs:

#             #item_data = dict(pair.split(': ') for pair in pairs)
#             try:
#                 item_name = pairs[2]
#             except IndexError:
#                 item_name = None
#             #full_type = item_data.get('fullType')
#             #item_name = item_data.get('itemName')

#             if item_name:

#                 prompt += re.match("displayName: (.*)", item_name)[1]

#                 counter += 1

#                 if counter > 10:
#                     print("_____________________________________________________")
#                     print(prompt)
#                     z = llm.create_chat_completion(
#                         messages = [
#                             {"role": "system", 
#                             "content": "I'm building an economy in a game. I will provide you with the name of a single item and you must give me its price in dollars. I will provide you with a list of items. Your answer will be formatted like NAME OF THE ITEM: $PRICE"},
#                             {
#                                 "role": "user",
#                                 "content": prompt
#                             }
#                         ]
#                     )
#                     print(z['choices'][0]['message']['content'])

#                     counter = 0
#                     prompt = ""
#                 else:
#                     prompt += ", "


