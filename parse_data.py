import re
import json

with open('items.json') as json_file:
    data = json.load(json_file)


window_size = 50


def get_items_tab(last_id : int, window_size : int):
    next_id = last_id + window_size
    return str(data[last_id : next_id])

for i in range(0, len(data), 50):
    print(str(data[i:i+50]))
    print("_______________________________")


# for d in data:
#     name = d['name']



# def return_item_names():
#     item_names = []
#     with open('new_items.txt', 'r') as file:
#         for line in file:
#             pairs = line.strip().split(", ")
#             if pairs:
#                 try:
#                     item_name = pairs[2]
#                 except IndexError:
#                     item_name = None

#                 if item_name:
#                     item_names.append(re.match("displayName: (.*)", item_name)[1])
#     return item_names


