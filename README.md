# Secure Password Manager 🔐

A simple password manager built using Python that securely stores website login credentials using encryption.

## Features

- Master password authentication
- Encrypted password storage
- Add, view, and delete saved accounts
- Generate strong random passwords
- Change the master password

## Technologies Used

- Python
- Cryptography
- JSON

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/YOUR-USERNAME/secure-password-manager.git
   ```

2. Navigate to the project folder:

   ```bash
    secure-password-manager
   ```

3. Install the required dependency:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python main.py
   ```

## Project Structure

```text
secure-password-manager/
├── main.py
├── encryption.py
├── password_generator.py
├── vault.py
├── requirements.txt
└── README.md
```

The `password_vault.json` file is created automatically when the application runs for the first time.

## How It Works

The application uses a master password to derive an encryption key. Saved login credentials are encrypted before being stored in a local JSON file.

Users can unlock the vault to manage their saved accounts and generate strong passwords.

## Security Note

This project was developed for educational purposes as a Python mini project. It is not a fully audited password manager. Use test credentials while experimenting, and keep backups of your encrypted vault.

## License

This project is available for educational and learning purposes.
