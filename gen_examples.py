from pydantic.v1 import BaseModel, ConfigDict, Field
from typing_extensions import Literal
from enum import Enum
from langchain.prompts import PromptTemplate

from zomboid_selector import ZomboidItemSelector
from zomb_gen_common import OutputEnum, Tags



class ExamplesModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    fullType: str = Field(..., alias='fullType')
    name: str = Field(..., alias='name')
    categories: str = "None"
    weight: str = "None"

    output: str


def get_output(t : OutputEnum, val_price : int = None, val_tag : str = None):
    out_type = 'price' if t==OutputEnum.PRICE else 'tag'
    val = val_price if t==OutputEnum.PRICE else val_tag
    return f"{{'{out_type}':'{val}'}}"

def get_examples(t : OutputEnum):

    return [
         ### ESSENTIALS
        ExamplesModel(fullType="Base.GranolaBar", name="Granola Bar", categories="[Food]", weight='0.2',
                  output=get_output(t, val_price=20, val_tag=Tags.food)).dict(),

        ExamplesModel(fullType="Base.BaseballBat", name="Baseball Bat", weight='2', categories="[Blunt, Sports]",
                    output=get_output(t, val_price=200, val_tag=Tags.weapon)).dict(),

        ExamplesModel(fullType="Base.ShotgunSawnoff", name="Sawed-Off Double Barrel Shotgun", weight='3', categories="[Weapon]",
                    output=get_output(t, val_price=1500, val_tag=Tags.weapon)).dict(),

        ExamplesModel(fullType='Base.Bullets9mmBox', name="Box of 9mm Rounds", weight='0.2', categories="[Ammo]",
                    output=get_output(t, val_price=250, val_tag=Tags.ammo)).dict(),

        ExamplesModel(fullType="Base.Bullets9mm", name="9mm Round", weight='0.0099', categories="[Ammo]",
                    output=get_output(t, val_price=9, val_tag=Tags.ammo)).dict(),


        ### SKILL BOOKS
        ExamplesModel(fullType="Base.BookBlacksmith1", name="Blacksmith Vol. 1", weight='0.8', categories="[SkillBook]",
                    output=get_output(t, val_price=150, val_tag=Tags.skill_book)).dict(),

        ExamplesModel(fullType="Base.BookBlacksmith2", name="Blacksmith Vol. 2", weight='0.8', categories="[SkillBook]",
                    output=get_output(t, val_price=200, val_tag=Tags.skill_book)).dict(),

        ExamplesModel(fullType="Base.BookBlacksmith3", name="Blacksmith Vol. 3", weight='0.8', categories="[SkillBook]",
                    output=get_output(t, val_price=300, val_tag=Tags.skill_book)).dict(),


        ExamplesModel(fullType="Base.BookBlacksmith4", name="Blacksmith Vol. 4", weight='0.8', categories="[SkillBook]",
                    output=get_output(t, val_price=500, val_tag=Tags.skill_book)).dict(),

        ExamplesModel(fullType="Base.BookBlacksmith5", name="Blacksmith Vol. 5", weight='0.8', categories="[SkillBook]",
                    output=get_output(t, val_price=600, val_tag=Tags.skill_book)).dict(),

        ### Bags as clothing




        ExamplesModel(fullType="Base.Bag_DuffelBagTINT", name="Duffel Bag", weight='1', categories="[Bag]",
                    output=get_output(t, val_price=500, val_tag=Tags.clothing)).dict(),

        ExamplesModel(fullType="Base.Bag_ALICEpack", name="Large Backpack", weight='2', categories="[Bag]",
                    output=get_output(t, val_price=800, val_tag=Tags.clothing)).dict(),

        ExamplesModel(fullType="Base.Bag_BigHikingBag", name="Big Hiking Bag", weight='1.5', categories="[Bag]",
                    output=get_output(t, val_price=1000, val_tag=Tags.clothing)).dict(),

        ### Food
        ExamplesModel(fullType="Base.CookieChocolateChip", name="Chocolate Chip Cookie", categories="[Food]", weight='0.1',
                    output=get_output(t, val_price=5, val_tag=Tags.food)).dict(),

        ExamplesModel(fullType="Base.Corn", name="Corn", categories="[Food]", weight='0.2',
                    output=get_output(t, val_price=2, val_tag=Tags.food)).dict(),
        ### Random Junk
        
        ExamplesModel(fullType="Base.ToiletPaper", name="Toilet Paper", weight='0.2', categories="[Junk]",
                    output=get_output(t, val_price=5, val_tag=Tags.various)).dict(),

        ExamplesModel(fullType="ATA2.ATA2ItemContainer", name="ATA2ItemContainer", weight='2', categories="[Tuning]",
                    output=get_output(t, val_price=150, val_tag=Tags.car_parts)).dict(),

        ExamplesModel(fullType="Base.CanoePadel", name="Canoe Paddle", weight='2', categories="[Improvised, Blunt, Sports]",
                    output=get_output(t, val_price=250, val_tag=Tags.weapon)).dict(),


        ### Guns
        ExamplesModel(fullType="Base.AssaultRifle", name="M16 Assault Rifle", weight='4', categories="[Weapon]",
                    output=get_output(t, val_price=2500, val_tag=Tags.weapon)).dict(),
        ExamplesModel(fullType="Base.AK47", name="AK47 Assault Rifle", weight='4.1', categories="[Weapon]",
                    output=get_output(t, val_price=2400, val_tag=Tags.weapon)).dict(),


        ## Beaver example

        ExamplesModel(fullType="Base.Tshirt_BBB_SittingBeaver", name="Sitting Beaver T-Shirt", weight='1', categories="[Clothing]",
                    output=get_output(t, val_price=2500, val_tag=Tags.various)).dict(),


        # DIRTY VS NOT DIRTY
        ExamplesModel(fullType="Base.Bandage", name="Bandage", weight='0.1', categories="[FirstAid]",
                    output=get_output(t, val_price=100, val_tag=Tags.first_aid)).dict(),
        ExamplesModel(fullType="Base.BandageDirty", name="Dirty Bandage", weight='0.1', categories="[FirstAid]",
                    output=get_output(t, val_price=10, val_tag=Tags.first_aid)).dict(),


        # Stuff that shouldn't cost that much
        ExamplesModel(fullType="Base.Jumper_DiamondPatternTINT", name="Diamond-pattern Sweater", weight='1', categories="[Clothing]",
                    output=get_output(t, val_price=80, val_tag=Tags.clothing)).dict(),
    ]


def setup_examples(gen_type : OutputEnum):

    # Setup examples
    example_template ="""
        Input:
        - FullType = {fullType}
        - Name = {name}
        - Weight = {weight}
        - Categories = {categories}

        Output:
        [{{{output}}}]
        """
    
    example_prompt = PromptTemplate(
        input_variables=["fullType", "name", "weight", "categories", "output"],
        template=example_template
    )

    examples = get_examples(gen_type)
    return example_prompt, ZomboidItemSelector(examples, 2)

