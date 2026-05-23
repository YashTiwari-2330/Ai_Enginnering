from __future__ import annotations

import os
from dataclasses import dataclass
from hashlib import pbkdf2_hmac
from typing import Any
from uuid import uuid4

from crypto_utils import derive_key_from_pin, decrypt_json, encrypt_json
from db_utils import next_account_number


def _b64e(raw: bytes) -> str:
    import base64

    return base64.b64encode(raw).decode("ascii")


@dataclass
class Transaction:
    tx_id: str
    ts: str
    kind: str  # deposit|withdraw
    amount: float
    note: str | None = None


class Account:
    """In-memory account facade. Sensitive state is stored encrypted in JSON."""

    def __init__(
        self,
        *,
        account_id: str,
        name: str,
        number: int,
        pin_salt_b64: str,
        enc_salt_b64: str,
        pin_hash_b64: str,
        enc_blob: dict[str, Any],
        txs: list[dict[str, Any]] | None = None,
    ):
        self.account_id = account_id
        self.name = name
        self.number = int(number)
        self.pin_salt_b64 = pin_salt_b64
        self.enc_salt_b64 = enc_salt_b64
        self.pin_hash_b64 = pin_hash_b64
        self.enc_blob = enc_blob
        self._txs = txs

    @staticmethod
    def create_new(*, db: dict[str, Any], name: str, pin: str, starting_balance: float) -> dict[str, Any]:
        if not name.strip():
            raise ValueError("Name is required")
        pin = str(pin)
        if len(pin) < 4:
            raise ValueError("PIN must be at least 4 characters")

        pin_salt = os.urandom(16)
        enc_salt = os.urandom(16)

        # Hash the PIN (store only hash)
        pin_hash = pbkdf2_hmac("sha256", pin.encode("utf-8"), pin_salt, 200_000, dklen=32)

        key_ctx = derive_key_from_pin(pin, enc_salt)

        from datetime import datetime, timezone

        payload = {
            "balance": float(starting_balance),
            "transactions": [
                {
                    "tx_id": str(uuid4()),
                    "ts": datetime.now(timezone.utc).isoformat(),
                    "kind": "init",
                    "amount": float(starting_balance),
                    "note": "account created",
                }
            ],
        }
        enc_blob = encrypt_json(payload, key=key_ctx.enc_key)

        account_id = str(uuid4())
        number = next_account_number(db)

        record = {
            "account_id": account_id,
            "name": name,
            "number": number,
            "pin": {
                "salt": _b64e(pin_salt),
                "hash": _b64e(pin_hash),
            },
            "encryption": {
                "salt": _b64e(enc_salt),
                "blob": enc_blob,
            },
        }
        return record

    def verify_pin(self, pin: str) -> bool:
        import base64

        pin = str(pin)
        if len(pin) < 1:
            return False

        pin_salt = base64.b64decode(self.pin_salt_b64.encode("ascii"))
        expected_hash = base64.b64decode(self.pin_hash_b64.encode("ascii"))
        actual_hash = pbkdf2_hmac("sha256", pin.encode("utf-8"), pin_salt, 200_000, dklen=32)
        return actual_hash == expected_hash

    def _decrypt_payload(self, pin: str) -> dict[str, Any]:
        import base64

        enc_salt = base64.b64decode(self.enc_salt_b64.encode("ascii"))
        ctx = derive_key_from_pin(pin, enc_salt)
        payload = decrypt_json(self.enc_blob, key=ctx.enc_key)
        return payload

    def _encrypt_payload(self, pin: str, payload: dict[str, Any]) -> dict[str, Any]:
        import base64

        enc_salt = base64.b64decode(self.enc_salt_b64.encode("ascii"))
        ctx = derive_key_from_pin(pin, enc_salt)
        return encrypt_json(payload, key=ctx.enc_key)

    def get_balance(self, pin: str) -> float:
        if not self.verify_pin(pin):
            raise PermissionError("Invalid PIN")
        payload = self._decrypt_payload(pin)
        return float(payload.get("balance", 0.0))

    def deposit(self, pin: str, amount: float, *, note: str | None = None) -> float:
        if not self.verify_pin(pin):
            raise PermissionError("Invalid PIN")
        amt = float(amount)
        if amt <= 0:
            raise ValueError("Deposit amount must be > 0")

        from datetime import datetime, timezone

        payload = self._decrypt_payload(pin)
        payload["balance"] = float(payload.get("balance", 0.0)) + amt
        payload.setdefault("transactions", []).append(
            {
                "tx_id": str(uuid4()),
                "ts": datetime.now(timezone.utc).isoformat(),
                "kind": "deposit",
                "amount": amt,
                "note": note,
            }
        )
        self.enc_blob = self._encrypt_payload(pin, payload)
        return float(payload["balance"])

    def withdraw(self, pin: str, amount: float, *, note: str | None = None) -> float:
        if not self.verify_pin(pin):
            raise PermissionError("Invalid PIN")
        amt = float(amount)
        if amt <= 0:
            raise ValueError("Withdrawal amount must be > 0")

        from datetime import datetime, timezone

        payload = self._decrypt_payload(pin)
        bal = float(payload.get("balance", 0.0))
        if bal < amt:
            raise ValueError("Insufficient balance")
        payload["balance"] = bal - amt
        payload.setdefault("transactions", []).append(
            {
                "tx_id": str(uuid4()),
                "ts": datetime.now(timezone.utc).isoformat(),
                "kind": "withdraw",
                "amount": amt,
                "note": note,
            }
        )
        self.enc_blob = self._encrypt_payload(pin, payload)
        return float(payload["balance"])

    def get_transactions(self, pin: str) -> list[dict[str, Any]]:
        if not self.verify_pin(pin):
            raise PermissionError("Invalid PIN")
        payload = self._decrypt_payload(pin)
        return list(payload.get("transactions", []))

    def change_pin(self, current_pin: str, new_pin: str) -> None:
        import base64

        current_pin = str(current_pin)
        new_pin = str(new_pin)
        if len(new_pin) < 4:
            raise ValueError("New PIN must be at least 4 characters")
        if not self.verify_pin(current_pin):
            raise PermissionError("Invalid current PIN")

        # re-derive encryption blob using same encryption salt but new pin
        payload = self._decrypt_payload(current_pin)

        pin_salt = os.urandom(16)
        pin_hash = pbkdf2_hmac("sha256", new_pin.encode("utf-8"), pin_salt, 200_000, dklen=32)

        self.pin_salt_b64 = _b64e(pin_salt)
        self.pin_hash_b64 = _b64e(pin_hash)

        # Encrypt payload with new pin-derived key (encryption salt stays the same)
        self.enc_blob = self._encrypt_payload(new_pin, payload)

