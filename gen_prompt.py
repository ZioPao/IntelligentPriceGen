from zomb_gen_common import OutputEnum


def get_suffix(t : OutputEnum):

    if t == OutputEnum.TAG:
        return """
########## [END EXAMPLES] ############

########## [START PREVIOUS DATA] ############
Use this ONLY if it seems relevant to the current item

{prevData}

########## [END PREVIOUS DATA] ############

Based on the data I'm giving you try to guess a tag for it.
Choose one of the following tags
[START TAGS]
- WEAPON
- AMMO
- CLOTHING
- MILITARY_CLOTHING
- FOOD
- FIRST_AID
- VARIOUS
- CAR_PARTS
- SKILL_BOOK
- FURNITURE
- TOOL
[END TAGS]

Keep in mind the following rules when deciding the price:
- Don't just copy the category for the tag field
- If the item in previous data same shares a lot of similiarity in the data, re-use the same tag
- If an item doesn't have Weapon in their category, it cannot have the tag WEAPON
- If there's no tag that seems to make sense for that item, use VARIOUS.

Format the output data as such: 
[
    {{ 'tag': string }}
]
Return ONLY ONE ITEM, do not make up new items.

############ [START INPUT DATA] ###############

- FullType = {fullType}, 
- Name = {name},
- Weight = {weight},
- Categories = {categories},

############ [END INPUT DATA] ###############

            """
    else:
        return"""
########## [END EXAMPLES] ############

########## [START PREVIOUS DATA] ############
Use this ONLY if it seems relevant to the current item

{prevData}

########## [END PREVIOUS DATA] ############

Based on the data I'm giving you try to guess a price.
Price must be an integer.

Keep in mind the following rules when deciding the price:
- Price can never be 0
- Price for a single item can't exceed 10000
- Clips should be priced at around 200
- Ammo boxes should be priced at around 600
- Bullet should be priced lower than 75
- If the item has Junk in their category, the price should be lower than 10
- If the item has Food in their category, the price should be between 5 and 100. Use the weight to guess how high it should be
- If the item in previous data same shares a lot of similiarity in the data, keep the price close

Format the output data as such: 
[
    {{ 'price': int }}
]
Return ONLY ONE ITEM, do not make up new items.


############ [START INPUT DATA] ###############

- FullType = {fullType}
- Name = {name}
- Weight = {weight}
- Categories = {categories}

############ [END INPUT DATA] ###############

"""