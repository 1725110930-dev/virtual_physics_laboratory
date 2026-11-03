"""Capa de acceso a PostgreSQL (Supabase).

Cada operación abre una conexión, ejecuta y cierra. Para un proyecto de este
tamaño es suficiente y evita dejar conexiones colgadas. Si más adelante hay
mucha carga, se puede cambiar por un pool de conexiones.
"""

import os
from contextlib import contextmanager

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

_REQUIRED_VARS = (
    "SUPABASE_DB_HOST",
    "SUPABASE_DB_PORT",
    "SUPABASE_DB_NAME",
    "SUPABASE_DB_USER",
    "SUPABASE_DB_PASSWORD",
)


class DatabaseError(Exception):
    """Error de configuración, conexión o consulta."""


class Database:
    @staticmethod
    def _connection_params():
        missing = [name for name in _REQUIRED_VARS if not os.getenv(name)]
        if missing:
            raise DatabaseError(
                "Faltan variables de entorno: " + ", ".join(missing)
            )

        return {
            "host": os.getenv("SUPABASE_DB_HOST"),
            "port": os.getenv("SUPABASE_DB_PORT"),
            "dbname": os.getenv("SUPABASE_DB_NAME"),
            "user": os.getenv("SUPABASE_DB_USER"),
            "password": os.getenv("SUPABASE_DB_PASSWORD"),
            "sslmode": os.getenv("SUPABASE_DB_SSLMODE", "require"),
        }

    @staticmethod
    def get_connection():
        """Crea una conexión nueva a Supabase."""
        try:
            return psycopg2.connect(**Database._connection_params())
        except Exception as exc:
            raise DatabaseError(f"No se pudo conectar a Supabase: {exc}") from exc

    @staticmethod
    @contextmanager
    def connection():
        """Conexión con commit/rollback y cierre automáticos."""
        conn = Database.get_connection()
        try:
            yield conn
        except Exception:
            conn.rollback()
            raise
        else:
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def fetch_all(query, params=()):
        """Devuelve una lista de diccionarios."""
        with Database.connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(query, params)
                return [dict(row) for row in cur.fetchall()]

    @staticmethod
    def fetch_one(query, params=()):
        """Devuelve un diccionario o None."""
        with Database.connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(query, params)
                row = cur.fetchone()
                return dict(row) if row else None

    @staticmethod
    def execute(query, params=()):
        """Ejecuta INSERT/UPDATE/DELETE y devuelve las filas afectadas."""
        with Database.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount

    @staticmethod
    def execute_query(query, params=None):
        """Compatibilidad con el código anterior.

        Devuelve filas si la consulta produce resultados (SELECT, RETURNING)
        o True si es una escritura sin resultados.
        """
        with Database.connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(query, params or ())
                if cur.description is not None:
                    return [dict(row) for row in cur.fetchall()]
                return True

    @staticmethod
    def execute_many(query, params_list):
        """Ejecuta la misma sentencia para varios conjuntos de parámetros."""
        with Database.connection() as conn:
            with conn.cursor() as cur:
                psycopg2.extras.execute_batch(cur, query, params_list)
                return cur.rowcount
