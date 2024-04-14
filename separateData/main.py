import json

with open('input.json') as json_file:
    data = json.load(json_file)

data = sorted(data, key=lambda d: d['fullType'])



def fetchLoop(t):
    array = []
    for j in range(0, len(data), 1):
        fullType = data[j]["fullType"]
        d = data[j][t]

        array.append({'fullType' : fullType, t : d})
        


    with open("output/"+t+".json", 'w') as file:
        file.write(json.dumps(array, indent=4))
    return array

prices = fetchLoop('basePrice')
tags = fetchLoop('tag')

print(prices)
print(tags)
