from langchain_core.example_selectors.base import BaseExampleSelector
from thefuzz import fuzz
import json

class FullTypeSelector(BaseExampleSelector):
    def __init__(self, examples, amount):
        self.examples = examples
        self.amount = amount

    def add_example(self, example):
        self.examples.append(example)


    def select_examples(self, input_variables):
        # compare fulltype

        ratio_list = []

        new_full_type = input_variables['fullType']
        for example in self.examples:
            r = fuzz.ratio(example['fullType'], new_full_type)
            ratio_list.append({'ratio': r, 'example': example})

        # sort it
        sorted_list = sorted(ratio_list, key=lambda d: d['ratio'])[-self.amount:]
        best_matches = [x['example'] for x in sorted_list]

        return best_matches