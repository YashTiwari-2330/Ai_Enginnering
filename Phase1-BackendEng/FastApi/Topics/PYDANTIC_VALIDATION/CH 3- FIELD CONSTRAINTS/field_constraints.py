from pydantic import BaseModel, Field


class Student(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    age: int = Field(ge=1, le=120)
    grade: int = Field(ge=0, le=100)


student = Student(name="Aman", age=21, grade=95)
print(student)
