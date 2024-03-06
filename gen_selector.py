from langchain_core.example_selectors.base import BaseExampleSelector
from thefuzz import fuzz
import json

class FullTypeSelector(BaseExampleSelector):
    def __init__(self, examples):
        self.examples = examples

    def add_example(self, example):
        self.examples.append(example)


    def select_examples(self, input_variables):
        # compare fulltype
        new_full_type = input_variables['fullType']
        best_match = None
        prev_best_ratio = -1
        for example in self.examples:
            r = fuzz.ratio(example['fullType'], new_full_type)
            if r > prev_best_ratio:
                prev_best_ratio = r
                best_match = example

        return [best_match]