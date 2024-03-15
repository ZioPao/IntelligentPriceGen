import json
import re


with open('output/prices.json') as json_file:
    prices_dict = json.load(json_file)

with open('output/tags.json') as json_file:
    tags_dict = json.load(json_file)


# Sort dicts
tags_dict = sorted(tags_dict, key=lambda d: d['fullType'])
prices_dict = sorted(prices_dict, key=lambda d: d['fullType'])

r = re.compile(r'sfx', re.I)

json_list = []
for i in range(0, len(prices_dict)):
    row_price = prices_dict[i]
    row_tags = tags_dict[i]

    fType = row_price['fullType']
    price = row_price['price']
    tag = row_tags['tag']

    temp_json = {}

    if fType != "Base.GranolaBar" and fType != "Base.WaterBottleFull" and fType != "Base.Cereal"\
            and fType != "Base.Butter" and fType != "Base.Baseballbat" and fType != "Base.Crowbar"\
            and fType != "Base.ShotgunSawnoff" and fType != "Base.ShotgunShellsBox"\
            and fType != "Base.ShotgunShellsBox" and fType != "Base.Pistol" and fType != "Base.9mmClip"\
            and fType != "Base.Bullets9mmBox" and fType != "Base.Bandage":

        if not r.findall(fType):

            temp_json['fullType'] = fType
            temp_json['tag'] = tag
            temp_json['basePrice'] = price

            json_list.append(temp_json)


# Add essential items with fixed prices


essentials = [
    {'fullType': "Base.GranolaBar",
     'tag': 'ESSENTIALS',
     'basePrice': 20},

    {'fullType': "Base.WaterBottleFull",
     'tag': 'ESSENTIALS',
     'basePrice': 50},

    {'fullType': "Base.Cereal",
     'tag': 'ESSENTIALS',
     'basePrice': 20},

    {'fullType': "Base.Butter",
     'tag': 'ESSENTIALS',
     'basePrice': 500},

    {'fullType': "Base.BaseballBat",
     'tag': 'ESSENTIALS',
     'basePrice': 200},

    {'fullType': "Base.Crowbar",
     'tag': 'ESSENTIALS',
     'basePrice': 1000},

    {'fullType': "Base.ShotgunSawnoff",
     'tag': 'ESSENTIALS',
     'basePrice': 1500},

    {'fullType': "Base.ShotgunShellsBox",
     'tag': 'ESSENTIALS',
     'basePrice': 250},

    {'fullType': "Base.Pistol",
     'tag': 'ESSENTIALS',
     'basePrice': 750},

    {'fullType': "Base.9mmClip",
     'tag': 'ESSENTIALS',
     'basePrice': 250},

    {'fullType': "Base.Bullets9mmBox",
     'tag': 'ESSENTIALS',
     'basePrice': 250},

    {'fullType': "Base.Bandage",
     'tag': 'ESSENTIALS',
     'basePrice': 100},

]

for i in range(0, len(essentials)):

    row = essentials[i]
    temp_json = {}
    temp_json['fullType'] = row['fullType']
    temp_json['tag'] = row['tag']
    temp_json['basePrice'] = row['basePrice']

    json_list.append(temp_json)



with open('output/shop_items.json', 'w') as file:
    # file.write(code)
    json.dump(json_list, file, indent=4)
