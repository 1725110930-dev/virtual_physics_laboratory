from config.database import Database

_COLUMNS = (
    "user_id, first_name, last_name, email, username, "
    "password_hash, role, is_active"
)


def find_by_identifier(identifier):
    """Busca un usuario por username o email (sin distinguir mayúsculas)."""
    return Database.fetch_one(
        f"""
        SELECT {_COLUMNS}
        FROM users
        WHERE lower(username) = lower(%s) OR lower(email) = lower(%s)
        LIMIT 1
        """,
        (identifier, identifier),
    )


def update_password_hash(user_id, password_hash):
    return Database.execute(
        "UPDATE users SET password_hash = %s WHERE user_id = %s",
        (password_hash, user_id),
    )
