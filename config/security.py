"""Hash MD5 de contraseñas.


"""

import hashlib


def hash_password(password: str) -> str:
    """Devuelve el MD5 en hexadecimal (32 caracteres)."""
    return hashlib.md5(password.encode("utf-8")).hexdigest()


def verify_password(stored: str, password: str) -> bool:
    """Compara el hash guardado con el MD5 de la contraseña recibida."""
    if not stored:
        return False
    return stored.lower() == hash_password(password)
