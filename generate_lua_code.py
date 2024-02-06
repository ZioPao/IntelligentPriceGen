import json

### Generate LUA Code
code_template = 'ShopItemsManager.AddItem("{fType}", {{["RANDOM"] = true}}, {basePrice}, 1, 0.25)'


with open('output/dict_prices_2.json') as json_file:
    prices_dict = json.load(json_file)


code = ""
for i in range(0, len(prices_dict)):
    row = prices_dict[i]
    fType = row['fullType']
    if fType != "Base.GranolaBar" and fType != "Base.WaterBottleFull" and fType != "Base.Cereal" and fType != "Base.Butter" and fType != "Base.Baseballbat" and fType != "Base.Crowbar" and fType != "Base.ShotgunSawnoff" and fType != "Base.ShotgunShellsBox" and fType != "Base.ShotgunShellsBox" and fType != "Base.Pistol" and fType != "Base.9mmClip" and fType != "Base.Bullets9mmBox" and fType != "Base.Bandage":

        code += code_template.format(fType=row['fullType'], basePrice=row['price']) + "\n"


with open('output/lua_code.txt', 'a+') as file:
    file.write(code)
