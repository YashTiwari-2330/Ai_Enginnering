from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)


product = Product(name="Laptop", price=799.99, stock=10)
print(product)
