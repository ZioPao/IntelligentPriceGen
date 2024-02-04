from llama_cpp import Llama
def get_prompt(prompt: str) -> str:
    return f"### User:\n{prompt}\n\n### Assistant:"

llm = Llama(model_path='models/solar-10.7b-instruct-v1.0-uncensored.Q4_K_M.gguf', n_batch=256, n_ctx=0, n_gpu_layers=40, verbose=True)
f_p = get_prompt("Write something nasty")

response = llm(prompt=f_p, stop=["</s>"], max_tokens=500, temperature=0.4)

print(response)