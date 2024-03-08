import tqdm
from common import get_data

data, prices = get_data()


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

def check_unique_tags(prices):
    tags = set([v['tag'] for v in prices])
    print(tags)