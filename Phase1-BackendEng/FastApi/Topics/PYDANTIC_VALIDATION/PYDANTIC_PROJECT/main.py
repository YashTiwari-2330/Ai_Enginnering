from fastapi import FastAPI
from models import Order

app = FastAPI()

@app.post("/orders")
def create_order(order:Order):

    return {
        "message" : "Order Crated Successfully",
        "data"    : order
    }