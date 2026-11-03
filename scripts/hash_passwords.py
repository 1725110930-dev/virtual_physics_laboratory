"""Migra las contraseñas guardadas en texto plano a PBKDF2.

Uso (desde la raíz del proyecto):

    python -m scripts.hash_passwords

Es idempotente: solo toca las contraseñas que no tienen el formato
`pbkdf2_sha256$...`.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import Database  # noqa: E402
from config.security import hash_password, needs_rehash  # noqa: E402


def main():
    users = Database.fetch_all(
        "SELECT user_id, username, password_hash FROM users ORDER BY user_id"
    )

    changed = 0
    for user in users:
        if needs_rehash(user["password_hash"]):
            Database.execute(
                "UPDATE users SET password_hash = %s WHERE user_id = %s",
                (hash_password(user["password_hash"]), user["user_id"]),
            )
            changed += 1

    print(f"{changed} contraseña(s) migrada(s) de {len(users)} usuario(s).")


if __name__ == "__main__":
    main()
