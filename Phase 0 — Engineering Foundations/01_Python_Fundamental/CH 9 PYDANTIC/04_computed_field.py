from pydantic import BaseModel, computed_field


class Circle(BaseModel):
    """Example showing computed fields in Pydantic."""

    radius: float

    @computed_field(return_type=float)
    @property
    def diameter(self) -> float:
        # Computed field derived from the radius.
        return self.radius * 2

    @computed_field(return_type=float)
    @property
    def area(self) -> float:
        # Area of the circle.
        return 3.14 * self.radius**2


circle = Circle(radius=5)
print("Radius:", circle.radius)
print("Diameter:", circle.diameter)
print("Area:", circle.area)

# Computed fields can be included in the serialized output.
print(circle.model_dump(include_computed_fields=True))
