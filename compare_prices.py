import json

with open('output/dict_prices_1.json') as j:
    data1 = json.load(j)
    

with open('output/dict_prices_2.json') as j:
    data2 = json.load(j)
    


for i in range(0, len(data1)):


    row1 = data1[i]
    row2 = data2[i]

    price1 = row1['price']
    price2 = row2['price']

    if price1 != price2:
        fType1 = row1['fullType']
        fType2 = row2['fullType']
        print("Model 1: {} => {}".format(fType1, price1))
        print("Model 2: {} => {}".format(fType2, price2))
        print("___________________________________________")