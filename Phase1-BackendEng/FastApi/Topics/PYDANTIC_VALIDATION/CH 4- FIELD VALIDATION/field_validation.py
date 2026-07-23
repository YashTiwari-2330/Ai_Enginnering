from pydantic import BaseModel, field_validator


class EmailModel(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("Email must contain '@'")
        return value


email_model = EmailModel(email="student@example.com")
print(email_model)
