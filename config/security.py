"""Hash y verificación de contraseñas usando solo la librería estándar.

Formato guardado en users.password_hash:

    pbkdf2_sha256$600000$<salt en base64>$<hash en base64>
"""

import base64
import hashlib
import hmac
import os

ALGORITHM = "pbkdf2_sha256"
ITERATIONS = 600_000
SALT_BYTES = 16


def hash_password(password: str) -> str:
    salt = os.urandom(SALT_BYTES)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, ITERATIONS
    )
    return "$".join(
        (
            ALGORITHM,
            str(ITERATIONS),
            base64.b64encode(salt).decode("ascii"),
            base64.b64encode(digest).decode("ascii"),
        )
    )


def verify_password(stored: str, password: str) -> bool:
    if not stored:
        return False

    if stored.startswith(ALGORITHM + "$"):
        try:
            _, iterations, salt_b64, digest_b64 = stored.split("$", 3)
            salt = base64.b64decode(salt_b64)
            expected = base64.b64decode(digest_b64)
            actual = hashlib.pbkdf2_hmac(
                "sha256", password.encode("utf-8"), salt, int(iterations)
            )
            return hmac.compare_digest(actual, expected)
        except (ValueError, TypeError):
            return False

    # Compatibilidad temporal: los datos de prueba se insertaron en texto
    # plano. Ejecuta `python -m scripts.hash_passwords` para migrarlos.
    return hmac.compare_digest(stored, password)


def needs_rehash(stored: str) -> bool:
    return not (stored or "").startswith(ALGORITHM + "$")
