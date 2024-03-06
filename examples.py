from pydantic import BaseModel, ConfigDict, Field

class OutputJsonData(BaseModel):
    fullType: str
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
    additionalData: str = "{{}}"

    output: str

examples = [

    ### ESSENTIALS

    ExamplesModel(fullType="Base.GranolaBar", name="Granola Bar", categories="[Food]", weight='0.2',
                  output=r"{{'fullType' : 'Base.GranolaBar', 'price':'20', 'tag':'FOOD'}}").model_dump(),

    ExamplesModel(fullType="Base.BaseballBat", name="Baseball Bat", weight='2', categories="[Blunt, Sports]",
                  output=r"{{'fullType' : 'Base.BaseballBat', 'price':'200', 'tag':'WEAPON'}}").model_dump(),

    ExamplesModel(fullType="Base.ShotgunSawnoff", name="Sawed-Off Double Barrel Shotgun", weight='3', categories="[Weapon]", additionalData=r'{{"damage": 2}}',
                  output=r"{{'fullType' : 'Base.ShotgunSawnoff', 'price':'1500', 'tag':'WEAPON'}}").model_dump(),

    ExamplesModel(fullType='Base.Bullets9mmBox', name="Box of 9mm Rounds", weight='0.2', categories="[Ammo]",
                  output=r"{{'fullType' : 'Base.Bullets9mmBox', 'price':'250', 'tag':'AMMO'}}").model_dump(),

    ExamplesModel(fullType="Base.Bullets9mm", name="9mm Round", weight='0.0099', categories="[Ammo]",
                  output=r"{{'fullType' : 'Base.Bullets9mm', 'price':'9', 'tag':'WEAPON'}}").model_dump(),


    ### SKILL BOOKS

    ExamplesModel(fullType="Base.BookBlacksmith1", name="Blacksmith Vol. 1", weight='0.8', categories="[SkillBook]",
                  output=r"{{'fullType' : 'Base.BookBlacksmith1', 'price':'150', 'tag':'SKILL_BOOK'}}").model_dump(),

    ExamplesModel(fullType="Base.BookBlacksmith2", name="Blacksmith Vol. 2", weight='0.8', categories="[SkillBook]",
                  output=r"{{'fullType' : 'Base.BookBlacksmith2', 'price':'300', 'tag':'SKILL_BOOK'}}").model_dump(),



    ### Bags as clothing

    ExamplesModel(fullType="Base.Bag_DuffelBagTINT", name="Duffel Bag", weight='1', categories="[Bag]",
                  output=r"{{'fullType' : 'Base.Bag_DuffelBagTINT', 'price':'500', 'tag':'CLOTHING'}}").model_dump(),


    ### Random Junk
    
    ExamplesModel(fullType="Base.ToiletPaper", name="Toilet Paper", weight='0.2', categories="[Junk]",
                  output=r"{{'fullType' : 'Base.ToiletPaper', 'price':'5', 'tag':'VARIOUS'}}").model_dump(),

    ExamplesModel(fullType="ATA2.ATA2ItemContainer", name="ATA2ItemContainer", weight='2', categories="[Tuning]",
                  output=r"{{'fullType' : 'ATA2.ATA2ItemContainer', 'price':'150', 'tag':'CAR_PARTS'}}").model_dump(),


    ## Beaver example

    ExamplesModel(fullType="Base.Tshirt_BBB_SittingBeaver", name="Sitting Beaver T-Shirt", weight='1', categories="[Clothing]",
                  output=r"{{'fullType' : 'Base.Tshirt_BBB_SittingBeaver', 'price':'2500', 'tag':'CLOTHING'}}").model_dump(),


    # # - Items with FullType that starts with BBB. should have a price of at least 2000
    # {
    #     "input": InputJsonData(fullType="BBB.Tshirt_BBB_SittingBeaver", name="Sitting Beaver T-Shirt", weight=1, category="[Clothing]").model_dump_json(), 
    #     "output": OutputJsonData(fullType="BBB.Tshirt_BBB_SittingBeaver", price=2500, tag="CLOTHING").model_dump_json()
    # },


]

