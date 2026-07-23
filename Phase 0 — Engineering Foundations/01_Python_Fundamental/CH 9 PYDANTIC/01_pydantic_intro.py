from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    """Simple example of a Pydantic model with field constraints."""

    name: str = Field(min_length=2, max_length=20)
    age: int = Field(gt=0, le=120)
    email: EmailStr


# Create a valid user object
user = User(name="Yash", age=25, email="yash@example.com")

print("User name:", user.name)
print("User age:", user.age)
print("User email:", user.email)

# Pydantic automatically validates the input before creating the object.
# If the data is invalid, it raises a ValidationError.
