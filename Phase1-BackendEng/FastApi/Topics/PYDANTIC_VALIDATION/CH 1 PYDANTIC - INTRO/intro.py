from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int


user = User(name="Yash", age=22)
print(user)
