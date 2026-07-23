from pydantic import BaseModel, model_validator


class Employee(BaseModel):
    """Example showing model-level validation with model_validator."""

    salary: float
    bonus: float
    total_pay: float | None = None

    @model_validator(mode="after")
    def check_payroll(self):
        # A model validator can check multiple fields together.
        if self.salary <= 0:
            raise ValueError("Salary must be greater than zero")
        if self.bonus < 0:
            raise ValueError("Bonus cannot be negative")

        self.total_pay = self.salary + self.bonus
        return self


# Valid example
employee = Employee(salary=50000, bonus=3000)
print("Salary:", employee.salary)
print("Bonus:", employee.bonus)
print("Total pay:", employee.total_pay)

# Invalid example: this will raise a ValidationError
try:
    Employee(salary=-1000, bonus=500)
except Exception as e:
    print("Model validation error:", e)
