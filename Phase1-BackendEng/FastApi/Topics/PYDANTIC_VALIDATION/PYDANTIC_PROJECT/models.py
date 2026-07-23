from typing import Annotated , Literal
from decimal import Decimal

from pydantic import (
    BaseModel,
    EmailStr,
    AnyUrl,
    Field,
    field_validator,
    model_validator,
    computed_field
)

#Custumer Model

class Customer(BaseModel):
    name : Annotated[
        str , Field(
            min_length=2,
            max_length=50,
            title= "Customer Name",
            description="Enter Customer Name :-"
        )
    ]

# Validate Email
    email : EmailStr

# Age must have 18
    age : Annotated[
        int , Field(
            gt = 18,
            le = 55,
            strict=True
        )
    ]
#Website URL
    website : AnyUrl


# Field Validator
# WhenValidating one field only
    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:

        if not value.replace(" " , "").isalpha():
            raise ValueError("Name should contain only latters")
        return value.title()
    
# =====================================================
# ADDRESS MODEL
# =====================================================

class Adress(BaseModel):

    city : str
    pincode : Annotated[
        str,
        Field(pattern=r"\d{6}$")
    ]

    country : str

# =====================================================
# PRODUCT MODEL
# =====================================================

class Product(BaseModel):
    name : str

    price : Annotated[
        Decimal,
        Field(gt=0)
    ]

    quantity : Annotated[
        int,
        Field(gt=0)
    ]

       # -----------------------------------------
    # computed_field
    # Calculate automatically
    # -----------------------------------------
    @computed_field
    @property
    def total(self) -> Decimal:
        return self.price * self.quantity
    
# =====================================================
# PAYMENT MODEL
# =====================================================

class Payment(BaseModel):
    method : Literal[
        "CARD",
        "UPI",
        "COD"
    ]

    card_number : str | None = None

     # -----------------------------------------
    # field_validator
    # Validate card number only
    # -----------------------------------------
    @field_validator("card_number")
    @classmethod
    def validate_card(cls , value):
        if value is None:
            return value
        
        if not value.isdigit():
            raise ValueError("Card should contain digits only")
        
        if len(value) != 16:
            raise ValueError("Card must containt 16 digits")
        
        return value
    
     # -----------------------------------------
    # model_validator
    # Validate multiple fields together
    # -----------------------------------------
    @model_validator(mode="after")
    def validate_payment(self):

        if self.method == "CARD" and self.card_number is None:
            raise ValueError("Card NUmber Requried")
        return self
    
# =====================================================
# ORDER MODEL
# =====================================================

class Order(BaseModel):
    customer : Customer
    shiping_adress : Adress
    product : list[Product]
    payment : Payment

    @computed_field
    @property
    def grand_total(self) -> Decimal:
        total = Decimal("0")

        for products in self.product:
            total += products.total
        return total
    