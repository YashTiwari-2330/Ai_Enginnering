from pydantic import BaseModel, Field, field_validator


class Product(BaseModel):
    """Example showing field validators in Pydantic."""

    name: str
    price: float = Field(ge=0)
    quantity: int = Field(gt=0)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        # Clean the name and make sure it is not empty.
        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("Product name cannot be empty")
        return cleaned_value.title()

    @field_validator("price")
    @classmethod
    def validate_price(cls, value: float) -> float:
        # Price should not be negative.
        if value < 0:
            raise ValueError("Price cannot be negative")
        return value


# Valid product example
product = Product(name=" laptop ", price=45000, quantity=2)
print(product)

# Invalid example: this will raise ValidationError
try:
    invalid_product = Product(name="   ", price=-10, quantity=0)
except Exception as e:
    print("Validation error:", e)
