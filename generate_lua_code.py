import json
import re

### Generate LUA Code
code_template = 'ShopItemsManager.AddItem("{fType}", {{["{tag}"] = true}}, {basePrice}, 1, 0.25)'


with open('output/prices.json') as json_file:
    prices_dict = json.load(json_file)

with open('output/tags.json') as json_file:
    tags_dict = json.load(json_file)


# Sort dicts
tags_dict = sorted(tags_dict, key=lambda d: d['fullType'])
prices_dict = sorted(prices_dict, key=lambda d: d['fullType'])

r = re.compile(r'sfx', re.I)

code = ""
for i in range(0, len(prices_dict)):
    row_price = prices_dict[i]
    row_tags = tags_dict[i]

    fType = row_price['fullType']
    price = row_price['price']
    tag = row_tags['tag']


    if fType != "Base.GranolaBar" and fType != "Base.WaterBottleFull"and fType != "Base.Cereal"\
        and fType != "Base.Butter" and fType != "Base.Baseballbat" and fType != "Base.Crowbar"\
    and fType != "Base.ShotgunSawnoff" and fType != "Base.ShotgunShellsBox"\
    and fType != "Base.ShotgunShellsBox" and fType != "Base.Pistol" and fType != "Base.9mmClip"\
    and fType != "Base.Bullets9mmBox" and fType != "Base.Bandage":

        if not r.findall(fType):
            code += code_template.format(fType=fType, tag=tag, basePrice=price) + "\n"

with open('output/shop_items.lua', 'a+') as file:
    file.write(code)

