"""Database service layer using Supabase PostgreSQL via psycopg2 with connection pooling."""
import os
import logging
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Connection pool — created once at import time, reused across every request.
# Min 1 / Max 10 connections; Render free tier handles this comfortably.
# ---------------------------------------------------------------------------
_pool: psycopg2.pool.ThreadedConnectionPool | None = None


def _get_pool() -> psycopg2.pool.ThreadedConnectionPool:
    """Return (or lazily create) the shared connection pool."""
    global _pool
    if _pool is None or _pool.closed:
        db_url = os.getenv("SUPABASE_DB_URL")
        if not db_url:
            raise DatabaseError(
                "SUPABASE_DB_URL environment variable is not set."
            )
        try:
            _pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=10,
                dsn=db_url,
                sslmode="require",
                connect_timeout=10,
            )
            logger.info("Database connection pool created successfully.")
        except Exception as exc:
            logger.error(f"Failed to create connection pool: {exc}")
            raise DatabaseError(f"Failed to connect to database: {exc}") from exc
    return _pool


# ---------------------------------------------------------------------------
# Custom exception
# ---------------------------------------------------------------------------
class DatabaseError(Exception):
    """Raised when a database operation fails."""


# ---------------------------------------------------------------------------
# Low-level query executor
# ---------------------------------------------------------------------------
class DatabaseService:

    @staticmethod
    def execute_query(query: str, params=None, fetch: bool = False):
        """
        Execute a parametrised SQL query using a pooled connection.

        Args:
            query:  SQL string (use %s placeholders).
            params: Tuple of parameters bound to the query.
            fetch:  If True, return result rows; otherwise return None.

        Returns:
            list[dict] | None
        """
        db_pool = _get_pool()
        conn = None
        cur = None
        try:
            conn = db_pool.getconn()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(query, params)
            result = cur.fetchall() if fetch else None
            conn.commit()
            return result

        except psycopg2.Error as exc:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {exc}")
            raise DatabaseError(str(exc)) from exc

        except Exception as exc:
            if conn:
                conn.rollback()
            logger.error(f"Unexpected database error: {exc}")
            raise DatabaseError(str(exc)) from exc

        finally:
            if cur:
                cur.close()
            if conn:
                db_pool.putconn(conn)   # Return connection to pool (not close!)


# ---------------------------------------------------------------------------
# Business-logic service
# ---------------------------------------------------------------------------
class ItemService:

    @staticmethod
    def get_all_items() -> list[dict]:
        """Return all items ordered newest-first."""
        query = "SELECT id, name FROM items ORDER BY id DESC"
        rows = DatabaseService.execute_query(query, fetch=True)
        return [{"id": row["id"], "name": row["name"]} for row in rows]

    @staticmethod
    def create_item(name: str) -> dict:
        """Insert a new item and return it."""
        query = """
            INSERT INTO items (name)
            VALUES (%s)
            RETURNING id, name
        """
        result = DatabaseService.execute_query(query, (name,), fetch=True)
        return {
            "id": result[0]["id"],
            "name": result[0]["name"],
            "message": "Item added successfully ✅",
        }

    @staticmethod
    def update_item(item_id: int, name: str) -> dict:
        """Update an existing item's name."""
        query = """
            UPDATE items
            SET name = %s
            WHERE id = %s
            RETURNING id, name
        """
        result = DatabaseService.execute_query(query, (name, item_id), fetch=True)
        if not result:
            raise ValueError("Item not found")
        return {
            "id": result[0]["id"],
            "name": result[0]["name"],
            "message": "Item updated successfully ✏️",
        }

    @staticmethod
    def delete_item(item_id: int) -> dict:
        """Delete an item by ID."""
        query = """
            DELETE FROM items
            WHERE id = %s
            RETURNING id
        """
        result = DatabaseService.execute_query(query, (item_id,), fetch=True)
        if not result:
            raise ValueError("Item not found")
        return {
            "id": result[0]["id"],
            "message": "Item deleted successfully 🗑️",
        }