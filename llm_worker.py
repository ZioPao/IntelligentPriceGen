from enum import Enum
from llama_cpp import Llama
import json


class LmmEnum(Enum):
    CapybaraHermes = {
        "path" : "models/capybarahermes-2.5-mistral-7b.Q5_K_M.gguf",
        "template" : '<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant',
        "hasSysMsg" : True
    }
    Solar = {
        "path": "models/solar-10.7b-instruct-v1.0-uncensored.Q4_K_M.gguf",
        "template": "### User:\n{prompt}\n\n### Assistant:",
        "hasSysMsg" : False
    }
    Dolphin = {
        "path": "models/dolphin-2.6-mistral-7b.Q3_K_M.gguf",
        "template": '<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant',
        "hasSysMsg" : True
    }
    NousCapybara = {
        "path": "models/nous-capybara-34b.Q5_K_S.gguf",
        "template": 'USER: {prompt} ASSISTANT:',
        "hasSysMsg" : False
    }
    Tess = {
        "path": "models/tess-34b-v1.5b.Q4_K_M.gguf",
        "template": "SYSTEM: {system_message}\nUSER:{prompt}\nASSISTANT:",
        "hasSysMsg" : True


    }

    def get_output_text(self, response):
        pass





class LmmWorker():
    def __init__(self, lmm_type : LmmEnum, grammar = None, n_ctx : int = 0, n_gpu_layers : int = -1, temperature : int = 0.25, n_batch : int = 256, print_tokens : bool = False):
        self.model_type = lmm_type
        self.model_path = lmm_type.value['path']
        self.template = lmm_type.value['template']
        self.hasSysMsg = lmm_type.value['hasSysMsg']
        self.llm = Llama(model_path=self.model_path, n_batch=n_batch, n_ctx=n_ctx, n_gpu_layers=n_gpu_layers, verbose=True, use_mlock=True)

        self.grammar = grammar
        self.temperature = temperature

        self.n_ctx = n_ctx
        

        self.print_tokens = print_tokens

    def set_sys_message(self, system_message : str):
        self.system_message = system_message

    def get_output_text(self, response):
        return response['choices'][0]['text']


    def run(self, prompt : str , system_message : str = None):
        if self.hasSysMsg:
            f_p = self.template.format(prompt=prompt, system_message=system_message)
        else:
            f_p = self.template.format(prompt=prompt)

        #print(f_p)

        isValid = False
        while not isValid:
            response = self.llm(prompt=f_p, stop=["</s>"], max_tokens=self.n_ctx, temperature=self.temperature, grammar=self.grammar)

            if self.print_tokens:
                usage = response['usage']
                print("Prompt Tokens: {0}, Completion Tokens: {1}, Total Tokens: {2}".format(usage["prompt_tokens"], usage["completion_tokens"], usage["total_tokens"]))


            try:
                text = json.loads(response['choices'][0]['text'])
                isValid = True
            except json.decoder.JSONDecodeError:
                print("Failed JSON parsing")
                print(response)


        return text