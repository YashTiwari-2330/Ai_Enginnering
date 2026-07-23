
""""
from __future__ import annotations

from typing import Optional

try:
    from pydantic import BaseModel, Field, model_validator
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "pydantic is not installed in this environment. Install it with: pip install pydantic"
    ) from exc


class Address(BaseModel):
    state: str = Field(..., min_length=2, max_length=30)
    city: str = Field(..., min_length=2, max_length=30)
    village: Optional[str] = Field(default=None, min_length=2, max_length=30)


class Account(BaseModel):
    # Basic account info
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., gt=0, lt=130)

    # Nested model
    address: Address

    # Cross-field validation that depends on nested data
    @model_validator(mode="after")
    def check_state_and_village(self) -> "Account":
        # Example business rule:
        # - If state is "Rajasthan" -> village must be provided
        # - For any other state -> village may be absent
        if self.address.state.strip().lower() == "rajasthan":
            if not self.address.village or not self.address.village.strip():
                raise ValueError("village is required when state is 'Rajasthan'")
        return self


if __name__ == "__main__":
    valid_payload = {
        "name": "Amit",
        "age": 25,
        "address": {
            "state": "Rajasthan",
            "city": "Jaipur",
            "village": "Chomu",
        },
    }

    invalid_payload_missing_village = {
        "name": "Amit",
        "age": 25,
        "address": {
            "state": "Rajasthan",
            "city": "Jaipur",
            # village missing -> should fail
        },
    }

    invalid_payload_bad_types = {
        "name": "A",
        "age": -5,
        "address": {
            "state": "R",
            "city": "J",
        },
    }

    print("--- VALID PAYLOAD ---")
    print(Account.model_validate(valid_payload))

    print("\n--- INVALID: missing village for Rajasthan ---")
    try:
        Account.model_validate(invalid_payload_missing_village)
    except Exception as e:
        print(e)

    print("\n--- INVALID: field constraints ---")
    try:
        Account.model_validate(invalid_payload_bad_types)
    except Exception as e:
        print(e)

"""