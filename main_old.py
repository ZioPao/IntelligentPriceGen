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


    # hermes prompt
    b_prompt = "<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant"
    sys_msg = "I'm creating an economy system in a game. I'll list some items by name and you'll give me a price in dollars. You must return it in such format: ITEM_NAME : $PRICE"
    f_p = b_prompt.format(system_message=sys_msg, prompt=prompt)

    #nous prompt
    
    b_p = "USER: {prompt} ASSISTANT:"
    sys_msg = "I'm creating an economy system in a game. I'll list some items by name and you'll give me a price in dollars. You must return it in such format, in a single line, with each element separated by a - : ITEM_NAME : $ PRICE"
    f_p = b_p.format(prompt=sys_msg + ". The list is " + prompt)


    z = llm(prompt=f_p, stop=["</s>"], max_tokens=150, temperature=0.4)

    print(z)
    #print(z['choices'][0]['text'])
    print("__________")
    #print(z['choices'][0]['message']['content'])






#llm = Llama(model_path='models/capybarahermes-2.5-mistral-7b.Q5_K_M.gguf',n_batch=1024, n_ctx=10000, n_gpu_layers=40, verbose=False)
llm = Llama(model_path='models/nous-capybara-34b.Q5_K_S.gguf',n_batch=512, n_ctx=150, n_gpu_layers=50, verbose=True)

names = return_item_names()

prompt = ""
counter = 0
for x in names:
    execute_llm(llm, x)

    # counter += 1
    # prompt += x
    # if counter > 100:
    #     execute_llm(llm, prompt)
    #     prompt = ""
    #     counter = 0
    # else:
    #     prompt += ", "






def setup_hermes():
    template = "<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant"


    sys_msg = "I'm creating an economy system in a game. I'll list some items by name and you'll give me a price in dollars. You must return it in such format: ITEM_NAME : $PRICE"
    f_p = b_prompt.format(system_message=sys_msg, prompt=prompt)


def setup_nous():
    
    b_p = "USER: {prompt} ASSISTANT:"
    sys_msg = "I'm creating an economy system in a game. I'll list some items by name and you'll give me a price in dollars. You must return it in such format, in a single line, with each element separated by a - : ITEM_NAME : $PRICE"
    f_p = b_p.format(prompt=sys_msg + ". The list is " + prompt)









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


