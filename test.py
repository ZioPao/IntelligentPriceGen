import json
def remove_fulltype(d):
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [remove_fulltype(v) for v in d]
    return {k: remove_fulltype(v) for k, v in d.items()
            if k not in {'fullType'}}

with open('items.json') as json_file:
    data = json.load(json_file)
    # Filter data, remove full type for now
    data = remove_fulltype(data)

print(data)