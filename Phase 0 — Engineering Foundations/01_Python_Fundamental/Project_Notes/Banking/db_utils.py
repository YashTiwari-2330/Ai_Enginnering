from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any


DB_PATH = os.path.join(os.path.dirname(__file__), "data.json")


def _empty_db() -> dict[str, Any]:
    return {
        "version": 1,
        "accounts": {},
    }


def load_db() -> dict[str, Any]:
    if not os.path.exists(DB_PATH) or os.path.getsize(DB_PATH) == 0:
        return _empty_db()
    with open(DB_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)
    if not raw:
        return _empty_db()
    if "accounts" not in raw:
        raw["accounts"] = {}
    return raw


def save_db(db: dict[str, Any]) -> None:
    tmp = DB_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    os.replace(tmp, DB_PATH)


def next_account_number(db: dict[str, Any]) -> int:
    """Return a unique 7-digit account number (1000000-9999999).

    Current implementation picks max(existing)+1, or starts at 1000000.
    If range overflows, it raises an error.
    """
    nums: list[int] = []
    for acc in db.get("accounts", {}).values():
        try:
            n = int(acc["number"])
            nums.append(n)
        except Exception:
            pass

    next_num = (max(nums) + 1) if nums else 1_000_000

    # Enforce 7 digits
    if next_num < 1_000_000:
        next_num = 1_000_000
    if next_num > 9_999_999:
        raise RuntimeError("No more 7-digit account numbers available")

    return next_num



def get_account_by_number(db: dict[str, Any], number: int) -> dict[str, Any] | None:
    for acc in db.get("accounts", {}).values():
        if int(acc.get("number")) == int(number):
            return acc
    return None


def update_account(db: dict[str, Any], account_id: str, account_record: dict[str, Any]) -> None:
    db.setdefault("accounts", {})[account_id] = account_record

