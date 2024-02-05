import json

with open('output/dict_prices_1.json') as j:
    data1 = json.load(j)
    

with open('output/dict_prices_2.json') as j:
    data2 = json.load(j)

with open('output/dict_prices_3.json') as j:
    data3 = json.load(j)


def check_fulltype(data_to_check):
    with open('items.json') as j:
        og_data = json.load(j)

    error_counter = 0
    for i in range(0, len(og_data)):
        og_ftype = og_data[i]['fullType']
        gen_ftype = data_to_check[i]['fullType']
        
        if og_ftype != gen_ftype:
            print("ID: " + str(i))
            print("Gen Ftype: {}".format(gen_ftype))
            print("OG FType: {}".format(og_ftype))
            error_counter += 1


    print("Amount of errors: " + str(error_counter) )



def compare_prices(data1, data2):
    for i in range(0, len(data1)):
        row1 = data2[i]
        row2 = data3[i]
        price1 = row1['price']
        price2 = row2['price']

        if price1 != price2:
            fType1 = row1['fullType']
            fType2 = row2['fullType']
            print("Model 1: {} => {}".format(fType1, price1))
            print("Model 2: {} => {}".format(fType2, price2))


check_fulltype(data3)