
import secrets
import string


def generate_password(length=16):
    """Generate a secure random password."""
    if length < 12:
        raise ValueError("Password must be at least 12 characters.")

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*()-_=+?"

    all_characters = lowercase + uppercase + digits + symbols

    # Ensure every character category is represented.
    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
        secrets.choice(symbols)
    ]

    password.extend(
        secrets.choice(all_characters)
        for _ in range(length - 4)
    )

    secrets.SystemRandom().shuffle(password)

    return "".join(password)
