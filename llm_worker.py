from enum import Enum
from llama_cpp import Llama
import json


class LmmEnum(Enum):
    CapybaraHermes = {
        "path" : "models/capybarahermes-2.5-mistral-7b.Q5_K_M.gguf",
        "template" : '<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant"',
        "hasSysMsg" : True
    }
    Solar = {
        "path": "models/solar-10.7b-instruct-v1.0-uncensored.Q4_K_M.gguf",
        "template": "### User:\n{prompt}\n\n### Assistant:",
        "hasSysMsg" : False
    }
    Dolphin = {
        "path": "models/dolphin-2.6-mistral-7b.Q3_K_M.gguf",
        "template": '<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant"',
        "hasSysMsg" : True
    }



class LmmWorker():
    def __init__(self, lmm_type : LmmEnum, grammar = None):
        self.model_path = lmm_type.value['path']
        self.template = lmm_type.value['template']
        self.hasSysMsg = lmm_type.value['hasSysMsg']
        self.llm = Llama(model_path=self.model_path, n_batch=256, n_ctx=0, n_gpu_layers=-1, verbose=True, use_mlock=True)

        self.grammar = grammar

    def set_sys_message(self, system_message : str):
        self.system_message = system_message



    def run(self, prompt : str , system_message : str = None):

        if self.hasSysMsg:
            f_p = self.template.format(prompt=prompt, system_message=system_message)
        else:
            f_p = self.template.format(prompt=prompt)

        #print(f_p)
        response = self.llm(prompt=f_p, stop=["</s>"], max_tokens=1500, temperature=0.25, grammar=self.grammar)
        try:
            text = json.loads(response['choices'][0]['text'])
        except json.decoder.JSONDecodeError:
            print("Failed JSON parsing")
            print(response)


        return text