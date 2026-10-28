
import os
import json
import base64
import getpass
import secrets
import string

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

VAULT_FILE = "password_vault.json"


def derive_key(master_password, salt):
    """Derive an encryption key from the master password."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000,
    )
    key = kdf.derive(master_password.encode("utf-8"))
    return base64.urlsafe_b64encode(key)


def create_vault(master_password):
    """Create a new encrypted vault."""
    salt = os.urandom(16)
    key = derive_key(master_password, salt)
    cipher = Fernet(key)

    encrypted_data = cipher.encrypt(b"[]")

    vault = {
        "salt": base64.b64encode(salt).decode("ascii"),
        "data": encrypted_data.decode("ascii")
    }

    with open(VAULT_FILE, "x", encoding="utf-8") as file:
        json.dump(vault, file, indent=4)

    print("Vault created successfully!")


def unlock_vault(master_password):
    """Decrypt and return saved login records."""
    with open(VAULT_FILE, "r", encoding="utf-8") as file:
        vault = json.load(file)

    salt = base64.b64decode(vault["salt"])
    key = derive_key(master_password, salt)
    cipher = Fernet(key)

    decrypted_data = cipher.decrypt(
        vault["data"].encode("ascii")
    )

    records = json.loads(decrypted_data.decode("utf-8"))

    if not isinstance(records, list):
        raise ValueError("Invalid vault format.")

    return records, cipher


def save_vault(records, cipher):
    """Encrypt and save the updated records."""
    encrypted_data = cipher.encrypt(
        json.dumps(records).encode("utf-8")
    )

    with open(VAULT_FILE, "r", encoding="utf-8") as file:
        vault = json.load(file)

    vault["data"] = encrypted_data.decode("ascii")

    temporary_file = VAULT_FILE + ".tmp"
    with open(temporary_file, "w", encoding="utf-8") as file:
        json.dump(vault, file, indent=4)

    os.replace(temporary_file, VAULT_FILE)


def generate_password(length=16):
    """Generate a strong random password."""
    if length < 12:
        raise ValueError("Password length must be at least 12.")

    alphabet = string.ascii_letters + string.digits + string.punctuation

    # Ensure at least one character from each category.
    password_chars = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation),
    ]

    password_chars.extend(
        secrets.choice(alphabet) for _ in range(length - 4)
    )

    # Securely shuffle the characters.
    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)


def main():
    print("\n=== SECURE PASSWORD MANAGER ===")

    if not os.path.exists(VAULT_FILE):
        print("No vault found. Create your master password.")
        master = getpass.getpass("New master password: ")

        if len(master) < 12:
            print("Use a master password of at least 12 characters.")
            return

        confirm = getpass.getpass("Confirm master password: ")

        if master != confirm:
            print("Passwords do not match.")
            return

        create_vault(master)

    master = getpass.getpass("Enter master password: ")

    try:
        records, cipher = unlock_vault(master)
    except InvalidToken:
        print("Incorrect master password or damaged vault.")
        return
    except (ValueError, KeyError, json.JSONDecodeError, OSError):
        print("Could not read the vault. Check the file.")
        return

    print("Vault unlocked successfully!")

    while True:
        print("\n1. Add login")
        print("2. View saved logins")
        print("3. Generate password")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            website = input("Website: ").strip()
            username = input("Username/email: ").strip()

            if not website or not username:
                print("Website and username are required.")
                continue

            password = getpass.getpass("Account password: ")

            records.append({
                "website": website,
                "username": username,
                "password": password
            })

            try:
                save_vault(records, cipher)
                print("Login saved securely!")
            except OSError:
                records.pop()
                print("Could not save the vault.")

        elif choice == "2":
            if not records:
                print("No saved logins.")
            else:
                for index, record in enumerate(records, start=1):
                    print(f"\nLogin {index}")
                    print("Website:", record["website"])
                    print("Username:", record["username"])
                    print("Password:", record["password"])

        elif choice == "3":
            try:
                length_text = input(
                    "Password length (minimum 12, default 16): "
                ).strip()
                length = int(length_text) if length_text else 16

                print("Generated password:", generate_password(length))
            except ValueError as error:
                print("Error:", error)

        elif choice == "4":
            print("Vault closed. Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
