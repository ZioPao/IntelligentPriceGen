import tqdm
import json


def check_fulltypes(data, prices):
    for i in range(0, len(data), 1):
        spliced_data = data[i:i+1][0]       # with the examples as I made them it becomes VERY specific with the format that it wants.
        #print(spliced_data)
        fullType = spliced_data['fullType']

        isFound = False
        for j in range(0, len(prices), 1):
            if fullType == prices[j]['fullType']:
                isFound = True
                break

        if not isFound:
            print(fullType + " NOT FOUND!!!!!!!!!!!!!!!!!")

def check_unique_tags(tags_json):
    tags = set([v['tag'] for v in tags_json])
    print(tags)

with open('output/tags.json') as json_file:
    tags_json = json.load(json_file)


check_unique_tags(tags_json=tags_json)