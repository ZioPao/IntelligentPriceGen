from pydantic.v1 import BaseModel, ConfigDict, Field

class OutputJsonData(BaseModel):
    #fullType: str
    price: int
    tag : str



    # def model_dump_json(self, *, indent: int | None = None, include: set[int] | set[str] | dict[int, any] | dict[str, any] | None = None, exclude: set[int] | set[str] | dict[int, any] | dict[str, any] | None = None, by_alias: bool = False, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, round_trip: bool = False, warnings: bool = True) -> str:
    #     return "{" + super().model_dump_json(indent=indent, include=include, exclude=exclude, by_alias=by_alias, exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none, round_trip=round_trip, warnings=warnings) + "}"

class ExamplesModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    fullType: str = Field(..., alias='fullType')
    name: str = Field(..., alias='name')
    categories: str = "None"
    weight: str = "None"
    #additionalData: str = "{{}}"

    output: str

examples = [

    ### ESSENTIALS

    ExamplesModel(fullType="Base.GranolaBar", name="Granola Bar", categories="[Food]", weight='0.2',
                  output=r"{{'price':'20', 'tag':'FOOD'}}").dict(),

    ExamplesModel(fullType="Base.BaseballBat", name="Baseball Bat", weight='2', categories="[Blunt, Sports]",
                  output=r"{{'price':'200', 'tag':'WEAPON'}}").dict(),

    ExamplesModel(fullType="Base.ShotgunSawnoff", name="Sawed-Off Double Barrel Shotgun", weight='3', categories="[Weapon]",
                  output=r"{{'price':'1500', 'tag':'WEAPON'}}").dict(),

    ExamplesModel(fullType='Base.Bullets9mmBox', name="Box of 9mm Rounds", weight='0.2', categories="[Ammo]",
                  output=r"{{'price':'250', 'tag':'AMMO'}}").dict(),

    ExamplesModel(fullType="Base.Bullets9mm", name="9mm Round", weight='0.0099', categories="[Ammo]",
                  output=r"{{'price':'9', 'tag':'WEAPON'}}").dict(),


    ### SKILL BOOKS

    ExamplesModel(fullType="Base.BookBlacksmith1", name="Blacksmith Vol. 1", weight='0.8', categories="[SkillBook]",
                  output=r"{{'price':'150', 'tag':'SKILL_BOOK'}}").dict(),

    ExamplesModel(fullType="Base.BookBlacksmith2", name="Blacksmith Vol. 2", weight='0.8', categories="[SkillBook]",
                  output=r"{{'price':'300', 'tag':'SKILL_BOOK'}}").dict(),

    ExamplesModel(fullType="Base.BookBlacksmith3", name="Blacksmith Vol. 3", weight='0.8', categories="[SkillBook]",
                  output=r"{{'price':'600', 'tag':'SKILL_BOOK'}}").dict(),

    ExamplesModel(fullType="Base.BookBlacksmith4", name="Blacksmith Vol. 4", weight='0.8', categories="[SkillBook]",
                  output=r"{{'price':'1200', 'tag':'SKILL_BOOK'}}").dict(),

    ExamplesModel(fullType="Base.BookBlacksmith5", name="Blacksmith Vol. 5", weight='0.8', categories="[SkillBook]",
                  output=r"{{'price':'2400', 'tag':'SKILL_BOOK'}}").dict(),

    ### Bags as clothing

    ExamplesModel(fullType="Base.Bag_DuffelBagTINT", name="Duffel Bag", weight='1', categories="[Bag]",
                  output=r"{{'price':'1200', 'tag':'CLOTHING'}}").dict(),

    ExamplesModel(fullType="Base.Bag_ALICEpack", name="Large Backpack", weight='2', categories="[Bag]",
                output=r"{{'price':'2000', 'tag':'CLOTHING'}}").dict(),

    ExamplesModel(fullType="Base.Bag_BigHikingBag", name="Big Hiking Bag", weight='1.5', categories="[Bag]",
                output=r"{{'price':'2500', 'tag':'CLOTHING'}}").dict(),



    ### Random Junk
    
    ExamplesModel(fullType="Base.ToiletPaper", name="Toilet Paper", weight='0.2', categories="[Junk]",
                  output=r"{{'price':'5', 'tag':'VARIOUS'}}").dict(),

    ExamplesModel(fullType="ATA2.ATA2ItemContainer", name="ATA2ItemContainer", weight='2', categories="[Tuning]",
                  output=r"{{'price':'150', 'tag':'CAR_PARTS'}}").dict(),


    ## Beaver example

    ExamplesModel(fullType="Base.Tshirt_BBB_SittingBeaver", name="Sitting Beaver T-Shirt", weight='1', categories="[Clothing]",
                  output=r"{{'price':'2500', 'tag':'CLOTHING'}}").dict(),


    # DIRTY VS NOT DIRTY
    ExamplesModel(fullType="Base.Bandage", name="Bandage", weight='0.1', categories="[FirstAid]",
                  output=r"{{'price':'100', 'tag':'FIRST_AID'}}").dict(),
    ExamplesModel(fullType="Base.BandageDirty", name="Dirty Bandage", weight='0.1', categories="[FirstAid]",
                  output=r"{{'price':'10', 'tag':'FIRST_AID'}}").dict(),



    # # - Items with FullType that starts with BBB. should have a price of at least 2000
    # {
    #     "input": InputJsonData(fullType="BBB.Tshirt_BBB_SittingBeaver", name="Sitting Beaver T-Shirt", weight=1, category="[Clothing]").model_dump_json(), 
    #     "output": OutputJsonData(fullType="BBB.Tshirt_BBB_SittingBeaver", price=2500, tag="CLOTHING").model_dump_json()
    # },


]

