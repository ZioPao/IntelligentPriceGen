from langchain_core.example_selectors.base import BaseExampleSelector
from thefuzz import fuzz

class ZomboidItemSelector(BaseExampleSelector):
    def __init__(self, examples, amount):
        self.examples = examples
        self.amount = amount

    def add_example(self, example):
        self.examples.append(example)


    def select_examples(self, input_variables):
        # compare fulltype

        ratio_list = []
        best_matches = []

        new_full_type = input_variables['fullType']
        new_cat = input_variables['categories']
        for example in self.examples:
            r = fuzz.ratio(example['fullType'], new_full_type)
            #r_cat = fuzz.ratio(example['categories'], new_cat)


            # TODO Having category as a check can work, but not with only a ratio check
            #r = (r_ft + r_cat)/2
            if r > 65:
                ratio_list.append({'ratio': r, 'example': example})

        # sort it
        sorted_list = sorted(ratio_list, key=lambda d: d['ratio'])[-self.amount:]
        best_matches = [x['example'] for x in sorted_list]

        return best_matches