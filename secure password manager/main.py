
import os

from encryption import create_vault, unlock_vault, VAULT_FILE
from password_generator import generate_password
from vault import add_account, view_accounts, delete_account

from cryptography.fernet import InvalidToken


def main():
    print("\n===================================")
    print("      SECURE PASSWORD MANAGER")
    print("===================================")

    # Step 1: Create a new vault if one does not exist.
    if not os.path.exists(VAULT_FILE):
        print("\nNo vault found. Create your master password.")

        master_password = input("Create master password: ")

        if len(master_password) < 12:
            print("Error: Use at least 12 characters.")
            return

        confirm_password = input("Confirm master password: ")

        if master_password != confirm_password:
            print("Error: Passwords do not match.")
            return

        try:
            create_vault(master_password)
            print("\nVault created successfully!")

        except FileExistsError:
            print("A vault already exists. Restart the program.")
            return

        except OSError as error:
            print("Could not create vault:", error)
            return

    # Step 2: Unlock the vault.
    master_password = input("\nEnter master password: ")

    try:
        records, cipher = unlock_vault(master_password)

    except InvalidToken:
        print("Incorrect master password or damaged vault.")
        return

    except (OSError, ValueError, KeyError, TypeError) as error:
        print("Could not open vault:", error)
        return

    print("\nVault unlocked successfully!")

    # Step 3: Display the main menu.
    while True:
        print("\n========== MAIN MENU ==========")
        print("1. Add account")
        print("2. View saved accounts")
        print("3. Delete account")
        print("4. Generate strong password")
        print("5. Exit")
        print("===============================")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_account(records, cipher)

        elif choice == "2":
            view_accounts(records)

        elif choice == "3":
            delete_account(records, cipher)

        elif choice == "4":
            try:
                length_text = input(
                    "Enter password length (minimum 12, default 16): "
                ).strip()

                length = int(length_text) if length_text else 16

                password = generate_password(length)

                print("\nGenerated password:", password)

            except ValueError as error:
                print("Invalid input:", error)

        elif choice == "5":
            print("\nVault closed. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
