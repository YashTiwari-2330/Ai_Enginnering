from __future__ import annotations

from typing import Any

from utils import load_db, save_db, load_account, persist_account, pretty_tx
import utils as app_utils


def prompt_int(message: str) -> int:
    while True:
        raw = input(message).strip()
        try:
            return int(raw)
        except ValueError:
            print("Enter a valid integer.")


def prompt_float(message: str) -> float:
    while True:
        raw = input(message).strip()
        try:
            return float(raw)
        except ValueError:
            print("Enter a valid number.")


def prompt_pin(message: str) -> str:
    pin = input(message).strip()
    return pin


def main() -> None:
    db = load_db()

    while True:
        print("\n--- Banking CLI (Encrypted JSON) ---")
        print("1. Create account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Show balance")
        print("5. Transaction history")
        print("6. Update PIN")
        print("7. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                name = input("Enter account holder name: ").strip()
                number = None
                pin = prompt_pin("Set PIN (min 4 chars): ")
                starting_balance = prompt_float("Enter starting balance: ")

                if starting_balance < 0:
                    print("Starting balance cannot be negative")
                    continue

                record = app_utils.create_account(db, name=name, number=number, pin=pin, starting_balance=starting_balance)
                db.setdefault("accounts", {})[record["account_id"]] = record
                save_db(db)
                print(f"Account created: {record['name']} (#{record['number']})")

            elif choice == "2":
                number = prompt_int("Enter account number: ")
                details = app_utils.get_public_account_details(db, number=number)
                if not details:
                    print("Account not found")
                    continue

                print(f"User details: {details['name']} (#{details['number']})")
                pin = prompt_pin("Enter PIN: ")
                amount = prompt_float("Enter amount to deposit: ")

                account = load_account(db, number=number)


                new_bal = account.deposit(pin, amount)
                persist_account(db, account)
                save_db(db)
                print(f"Deposit successful. New balance: {new_bal}")

            elif choice == "3":
                number = prompt_int("Enter account number: ")
                details = app_utils.get_public_account_details(db, number=number)
                if not details:
                    print("Account not found")
                    continue

                print(f"User details: {details['name']} (#{details['number']})")
                pin = prompt_pin("Enter PIN: ")
                amount = prompt_float("Enter amount to withdraw: ")

                account = load_account(db, number=number)


                new_bal = account.withdraw(pin, amount)
                persist_account(db, account)
                save_db(db)
                print(f"Withdrawal successful. New balance: {new_bal}")

            elif choice == "4":
                number = prompt_int("Enter account number: ")
                details = app_utils.get_public_account_details(db, number=number)
                if not details:
                    print("Account not found")
                    continue

                print(f"User details: {details['name']} (#{details['number']})")
                pin = prompt_pin("Enter PIN: ")

                account = load_account(db, number=number)


                bal = account.get_balance(pin)
                print(f"Current balance: {bal}")

            elif choice == "5":
                number = prompt_int("Enter account number: ")
                details = app_utils.get_public_account_details(db, number=number)
                if not details:
                    print("Account not found")
                    continue

                print(f"User details: {details['name']} (#{details['number']})")
                pin = prompt_pin("Enter PIN: ")

                account = load_account(db, number=number)


                txs = account.get_transactions(pin)
                print("\n--- Transactions ---")
                for tx in txs:
                    print(pretty_tx(tx))

            elif choice == "6":
                number = prompt_int("Enter account number: ")
                details = app_utils.get_public_account_details(db, number=number)
                if not details:
                    print("Account not found")
                    continue

                print(f"User details: {details['name']} (#{details['number']})")
                current_pin = prompt_pin("Enter current PIN: ")
                new_pin = prompt_pin("Enter new PIN (min 4 chars): ")

                account = load_account(db, number=number)


                account.change_pin(current_pin, new_pin)
                persist_account(db, account)
                save_db(db)
                print("PIN updated successfully")

            elif choice == "7":
                print("Goodbye!")
                break

            else:
                print("Invalid option. Choose 1-7.")

        except PermissionError as e:
            print(str(e))
        except Exception as e:
            print(f"Operation failed: {e}")


if __name__ == "__main__":
    main()

