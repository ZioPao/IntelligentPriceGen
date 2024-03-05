from llama_cpp import Llama
def get_prompt(prompt: str) -> str:
    return f"### User:\n{prompt}\n\n### Assistant:"

llm = Llama(model_path='models/solar-10.7b-instruct-v1.0-uncensored.Q4_K_M.gguf', n_batch=256, n_ctx=0, n_gpu_layers=40, verbose=True)
#
# f_p = get_prompt("You are a doctor, we're gonna do a roleplay:\n Please doctor, my penis stopped working, my wife started beating me and it won't get up anymore")
f_p = get_prompt("Sei un dottore, facciamo un gioco di ruolo:\n Buongiorno dottore, il mio pipino non si muove più da giorni, come faccio?")

response = llm(prompt=f_p, stop=["</s>"], max_tokens=500, temperature=0.4)

print(response['choices'][0]['text'])

# import json
# with open('data/items.json') as json_file:
#     data = json.load(json_file)
    

# print(len(data[-100:]))