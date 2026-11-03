"""Migra las contraseñas en texto plano a MD5.

Uso (desde la raíz del proyecto):

    python -m scripts.hash_passwords

Es idempotente: solo toca las contraseñas que todavía no son un MD5.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import Database  # noqa: E402
from config.security import hash_password  # noqa: E402

MD5_RE = re.compile(r"^[0-9a-f]{32}$")


def main():
    users = Database.fetch_all(
        "SELECT user_id, username, password_hash FROM users ORDER BY user_id"
    )

    changed = 0
    for user in users:
        stored = user["password_hash"] or ""
        if not MD5_RE.match(stored.lower()):
            Database.execute(
                "UPDATE users SET password_hash = %s WHERE user_id = %s",
                (hash_password(stored), user["user_id"]),
            )
            changed += 1

    print(f"{changed} contraseña(s) migrada(s) de {len(users)} usuario(s).")


if __name__ == "__main__":
    main()
