contact_details = {}


def normalize_name(name):
    return name.strip().lower()


def input_required(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field is required. Please enter a value.")


def input_optional(prompt):
    value = input(prompt).strip()
    return value if value else "N/A"


def get_contact_details():
    return {
        "name": input_required("Enter name: "),
        "phone": input_required("Enter phone number: "),
        "email": input_optional("Enter email: "),
        "address": input_optional("Enter address: "),
        "birthday": input_optional("Enter birthday: "),
        "notes": input_optional("Enter notes: "),
    }


def add_contact():
    contact = get_contact_details()
    key = normalize_name(contact["name"])

    if key in contact_details:
        print("Contact already exists.")
        return

    contact_details[key] = contact
    print("Contact added successfully.")


def print_contact(contact):
    print("-" * 35)
    print("Name     :", contact["name"])
    print("Phone    :", contact["phone"])
    print("Email    :", contact["email"])
    print("Address  :", contact["address"])
    print("Birthday :", contact["birthday"])
    print("Notes    :", contact["notes"])
    print("-" * 35)


def search_contact():
    search_value = input_required("Enter name or phone number to search: ").lower()

    for contact in contact_details.values():
        if search_value in contact["name"].lower() or search_value in contact["phone"]:
            print("Contact found:")
            print_contact(contact)
            return

    print("Contact not found.")


def update_contact():
    name = input_required("Enter contact name to update: ")
    key = normalize_name(name)

    if key not in contact_details:
        print("Contact not found.")
        return

    print("Press Enter to keep old value.")
    contact = contact_details[key]

    new_name = input(f"Name [{contact['name']}]: ").strip()
    new_phone = input(f"Phone [{contact['phone']}]: ").strip()
    new_email = input(f"Email [{contact['email']}]: ").strip()
    new_address = input(f"Address [{contact['address']}]: ").strip()
    new_birthday = input(f"Birthday [{contact['birthday']}]: ").strip()
    new_notes = input(f"Notes [{contact['notes']}]: ").strip()

    updated_contact = {
        "name": new_name or contact["name"],
        "phone": new_phone or contact["phone"],
        "email": new_email or contact["email"],
        "address": new_address or contact["address"],
        "birthday": new_birthday or contact["birthday"],
        "notes": new_notes or contact["notes"],
    }

    new_key = normalize_name(updated_contact["name"])
    if new_key != key and new_key in contact_details:
        print("Another contact with this name already exists.")
        return

    del contact_details[key]
    contact_details[new_key] = updated_contact
    print("Contact updated successfully.")


def delete_contact():
    name = input_required("Enter contact name to delete: ")
    key = normalize_name(name)

    if key in contact_details:
        del contact_details[key]
        print("Contact deleted successfully.")
    else:
        print("Contact not found.")


def display_contacts():
    if not contact_details:
        print("No contacts available.")
        return

    print("\nAll Contacts")
    print("=" * 35)
    for contact in sorted(contact_details.values(), key=lambda item: item["name"].lower()):
        print_contact(contact)


def display_menu():
    print("\nContact Book Menu")
    print("1. Add contact")
    print("2. Search contact")
    print("3. Update contact")
    print("4. Delete contact")
    print("5. Display all contacts")
    print("6. Exit")


def main():
    while True:
        display_menu()
        choice = input("Enter your choice number: ").strip()

        if choice == "1":
            add_contact()
        elif choice == "2":
            search_contact()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            delete_contact()
        elif choice == "5":
            display_contacts()
        elif choice == "6":
            print("Thank you for using Contact Book.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
