from pydantic.v1 import BaseModel, ConfigDict, Field
from enum import Enum
from typing_extensions import Literal
import json

########### ...
class OutputJsonPrice(BaseModel):
    price: int

class OutputJsonTag(BaseModel):
    tag : Literal[
        "AMMO", "FIRST_AID",
        "FURNITURE", "VARIOUS",
        "CLOTHING", "CAR_PARTS",
        "FOOD", "SKILL_BOOK",
        "WEAPON", "MILITARY_CLOTHING",
        "TOOL"]


class OutputEnum(Enum):
    PRICE = 1
    TAG = 2

class Tags(Enum):
    food = "FOOD"
    weapon = "WEAPON"
    ammo = "AMMO"
    skill_book = "SKILL_BOOK"
    clothing = "CLOTHING"
    various = "VARIOUS"
    car_parts = "CAR_PARTS"
    first_aid = "FIRST_AID"

########## DATA

PRICES_JSON_PATH = 'output/prices_noushermes2.json'

def get_data(path=PRICES_JSON_PATH):
    # Load data
    with open('data/items.json') as json_file:
        data = json.load(json_file)

    try:
        with open(path, 'r') as json_file:
            prices = json.load(json_file)
    except FileNotFoundError:
        prices = []

    data = sorted(data, key=lambda d: d['fullType'])
    prices = sorted(prices, key=lambda d: d['fullType'])
    return data, prices
