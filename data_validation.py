import json
from llm_worker import LmmEnum

price_path = 'output/prices_{}.json'

with open(price_path.format(LmmEnum.CapybaraHermes.name), 'r') as j:
    data1 = json.load(j)


with open(price_path.format(LmmEnum.Tess.name), 'r') as j:
    data2 = json.load(j)








def check_fulltype(path):
    with open('items.json') as j:
        og_data = json.load(j)

    with open(path, 'r') as file:
        data_to_check = json.load(file)



    error_counter = 0
    for i in range(0, len(og_data)):
        og_ftype = og_data[i]['fullType']
        gen_ftype = data_to_check[i]['fullType']
        
        if og_ftype != gen_ftype:
            print("ID: " + str(i))
            print("Gen Ftype: {}".format(gen_ftype))
            print("OG FType: {}".format(og_ftype))
            error_counter += 1

            with open("output/fixed.json", 'w') as file:
                data_to_check[i]['fullType'] = og_ftype
                file.write(json.dumps(data_to_check, indent=4))

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


check_fulltype(price_path.format(LmmEnum.CapybaraHermes.name))