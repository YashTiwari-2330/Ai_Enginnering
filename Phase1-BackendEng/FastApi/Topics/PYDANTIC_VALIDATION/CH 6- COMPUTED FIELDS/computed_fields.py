from pydantic import BaseModel, computed_field


class Circle(BaseModel):
    radius: float

    @computed_field
    @property
    def diameter(self) -> float:
        return self.radius * 2


circle = Circle(radius=5)
print(circle.diameter)
