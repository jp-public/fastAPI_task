from math import ceil
from fastapi import FastAPI
from pydantic import BaseModel, Field
from dateutil import parser
import datetime


FREE_DELIVERY = 10000 # bound for free delivery
MAX_FEE = 1500 # maximum for deliver fee
BASE_DISTANCE_FEE = 200 # base distance component of delivery fee
BASE_DISTANCE = 1000 #meters
DISTANCE_FEE = 100 # additional distance component of delivery fee
DISTANCE = 500 #meters
ITEM_SURCHARGE = 50 # extra charge for each additional item
FREE_ITEMS = 4 # number of items without additional charge
MIN_ORDER = 1000 # if order is below this, difference will be added to order
SURGE_FACTOR = 1.1 # factor for Friday afternoon surge

app = FastAPI(title="Delivery fee calculator made with FastAPI",
              description="Pre-assignment task for Wolt Summer 2022 Engineering Internships",
              version="0.1")


class DeliveryDetails(BaseModel):
    cart_value: int  = Field(None, description="Value of the shopping cart in cents.")
    delivery_distance: int = Field(None, description="The distance between the store and customer’s location in meters.")
    number_of_items: int = Field(None, description="The number of items in the customer's shopping cart.")
    time: str = Field(None, description="Order time in ISO 8601 format.")

    class Config:
        schema_extra = {
            "example": {
                "cart_value:": 790,
                "delivery_distance": 2235 ,
                "number_of_items": 4 ,
                "time:": "2021-01-16T13:00:00Z",
            }
        }


class DeliveryFee(BaseModel):
    delivery_fee: int = Field(None, description="Calculated delivery fee in cents.")

    class Config:
        schema_extra = {
            "example": {
                "delivery_fee:": 790
            }
        }


@app.post("/", response_model=DeliveryFee)
async def calculate_fee(details:  DeliveryDetails):
    if details.cart_value >= FREE_DELIVERY:
        fee_amount = 0
    else:
        distance_fee = BASE_DISTANCE_FEE + (max(0, ceil((details.delivery_distance-BASE_DISTANCE)/DISTANCE)) * DISTANCE_FEE)
        items_fee = max(0, (details.number_of_items - FREE_ITEMS) * ITEM_SURCHARGE)
        min_order_fee = max(0, MIN_ORDER - details.cart_value)
        fee_amount = min(MAX_FEE, distance_fee + items_fee + min_order_fee)
        order_time = parser.parse(details.time)
        if order_time.strftime('%A') == "Friday" and datetime.time(19) >= order_time.time() >= datetime.time(15):
            fee_amount = (min(MAX_FEE, int(fee_amount * SURGE_FACTOR)))
    fee = {"delivery_fee": fee_amount}
    return fee
