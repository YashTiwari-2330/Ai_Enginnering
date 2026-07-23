from pydantic import BaseModel, model_validator


class Order(BaseModel):
    quantity: int
    price: float

    @model_validator(mode="after")
    def validate_total(self):
        if self.quantity < 1:
            raise ValueError("Quantity must be at least 1")
        return self


order = Order(quantity=3, price=50)
print(order)
