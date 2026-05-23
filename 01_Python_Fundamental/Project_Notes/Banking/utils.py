from __future__ import annotations

import json
from typing import Any

from db_utils import get_account_by_number, load_db, save_db
from models import Account


def get_public_account_details(db: dict[str, Any], *, number: int) -> dict[str, Any] | None:
    rec = get_account_by_number(db, number)
    if not rec:
        return None
    return {
        "account_id": rec.get("account_id"),
        "name": rec.get("name"),
        "number": rec.get("number"),
    }



def create_account(db: dict[str, Any], *, name: str, number: int | None, pin: str, starting_balance: float) -> dict[str, Any]:
    # number is auto-assigned by Account.create_new for safety
    record = Account.create_new(db=db, name=name, pin=pin, starting_balance=starting_balance)
    return record


def load_account(db: dict[str, Any], *, number: int) -> Account | None:
    rec = get_account_by_number(db, number)
    if not rec:
        return None

    pin = rec["pin"]
    enc = rec["encryption"]
    return Account(
        account_id=rec["account_id"],
        name=rec["name"],
        number=rec["number"],
        pin_salt_b64=pin["salt"],
        pin_hash_b64=pin["hash"],
        enc_salt_b64=enc["salt"],
        enc_blob=enc["blob"],
    )


def persist_account(db: dict[str, Any], account: Account) -> None:
    # Write the current in-memory encrypted blob back into db record
    accounts = db.setdefault("accounts", {})
    accounts[account.account_id] = {
        "account_id": account.account_id,
        "name": account.name,
        "number": account.number,
        "pin": {
            "salt": account.pin_salt_b64,
            "hash": account.pin_hash_b64,
        },
        "encryption": {
            "salt": account.enc_salt_b64,
            "blob": account.enc_blob,
        },
    }


def pretty_tx(tx: dict[str, Any]) -> str:
    kind = tx.get("kind")
    amount = tx.get("amount")
    ts = tx.get("ts")
    note = tx.get("note")
    s = f"[{ts}] {kind}: {amount}"
    if note:
        s += f" ({note})"
    return s

