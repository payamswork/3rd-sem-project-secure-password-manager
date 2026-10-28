
from encryption import save_vault


def add_account(records, cipher):
    """Add a website login to the encrypted vault."""
    website = input("Website: ").strip()
    username = input("Username or email: ").strip()
    password = input("Account password: ")

    if not website or not username or not password:
        print("All fields are required.")
        return

    records.append({
        "website": website,
        "username": username,
        "password": password
    })

    try:
        save_vault(records, cipher)
        print("Account saved successfully!")

    except (OSError, ValueError):
        records.pop()
        print("Could not save the account.")


def view_accounts(records):
    """Display saved login details."""
    if not records:
        print("No accounts saved yet.")
        return

    for index, record in enumerate(records, start=1):
        print(f"\nAccount {index}")
        print("Website:", record["website"])
        print("Username:", record["username"])
        print("Password:", record["password"])


def delete_account(records, cipher):
    """Delete an account by its number."""
    if not records:
        print("No accounts to delete.")
        return

    view_accounts(records)

    try:
        number = int(input("\nEnter account number to delete: "))

        if number < 1 or number > len(records):
            print("Invalid account number.")
            return

        removed = records.pop(number - 1)

        try:
            save_vault(records, cipher)
            print("Account deleted successfully!")

        except (OSError, ValueError):
            records.insert(number - 1, removed)
            print("Could not save the changes.")

    except ValueError:
        print("Please enter a valid number.")
