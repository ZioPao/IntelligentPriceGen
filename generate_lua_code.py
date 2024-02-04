import json

### Generate LUA Code
code_template = 'ShopItemsManager.AddItem("{}", {{["{}"] = true}}, {}, 1, 0.25)'
with open('items.json') as json_file:
    data = json.load(json_file)

with open('test_prices.json') as json_file:
    prices_dict = json.load(json_file)



for i in range(0, len(data)):
    f_type = data[i]
    print(f_type)