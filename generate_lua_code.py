import json
import re

### Generate LUA Code
code_template = 'ShopItemsManager.AddItem("{fType}", {{["{tag}"] = true}}, {basePrice}, 1, 0.25)'


with open('output/prices_noushermes2.json') as json_file:
    prices_dict = json.load(json_file)


r = re.compile(r'sfx', re.I)


def generate_lua(use_tag=False):
    code = ""
    for i in range(0, len(prices_dict)):
        row = prices_dict[i]
        #print(row)
        fType = row['fullType']
        if fType != "Base.GranolaBar" and fType != "Base.WaterBottleFull"and fType != "Base.Cereal"\
            and fType != "Base.Butter" and fType != "Base.Baseballbat" and fType != "Base.Crowbar"\
        and fType != "Base.ShotgunSawnoff" and fType != "Base.ShotgunShellsBox"\
        and fType != "Base.ShotgunShellsBox" and fType != "Base.Pistol" and fType != "Base.9mmClip"\
        and fType != "Base.Bullets9mmBox" and fType != "Base.Bandage":

            if not r.findall(fType):
                if use_tag:
                    tag=row['tag']
                else:
                    tag="VARIOUS"
                    

                code += code_template.format(fType=row['fullType'], tag=tag, basePrice=row['price']) + "\n"
            else:
                print(row)

    with open('output/shop_items.lua', 'a+') as file:
        file.write(code)


generate_lua(use_tag=False)