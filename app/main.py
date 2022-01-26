from math import ceil
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

MAX_FEE = 1500
BASE_DISTANCE_FEE = 200
DISTANCE_FEE = 100
ITEM_SURCHARGE = 50
MIN_ORDER = 1000
SURGE_FACTOR = 1.1


class DeliveryDetails(BaseModel):
    cart_value: int
    delivery_distance: int
    number_of_items: int
    time: str


class DeliveryFee(BaseModel):
    delivery_fee: int


@app.post("/", response_model=DeliveryFee)
async def calculate_fee(details:  DeliveryDetails):
    if details.cart_value >= 10000:
        fee_amount = 0
    else:
        distance_fee = BASE_DISTANCE_FEE + (max(0, ceil((details.delivery_distance-1000)/500)) * DISTANCE_FEE)
        items_fee = max(0, (details.number_of_items - 4) * ITEM_SURCHARGE)
        order_fee = max(0, MIN_ORDER - details.cart_value)
        fee_amount = min(MAX_FEE, distance_fee + items_fee + order_fee)
    fee = {"delivery_fee": fee_amount}
    return fee
