"""
Utility to fix lightweight schema drift in the SQLite dev DB.

Usage:
    python fix_db_schema.py

What it does:
 - Reads `DATABASE_URL` from `config.settings`.
 - If the DB is SQLite, checks `PRAGMA table_info('goals')`.
 - If `category_id` column is missing, runs `ALTER TABLE goals ADD COLUMN category_id INTEGER`.

This is intended as a small, safe developer helper for testing environments only.
For production / long-lived projects, use proper migrations (Alembic).
"""
import os
import sqlite3
import sys

# Avoid importing full app config (pydantic Settings may raise on unexpected env vars).
# Read DATABASE_URL from environment if available, otherwise use default.
def _get_database_url_from_env():
    return os.getenv('DATABASE_URL') or os.getenv('HR_SYSTEM_DATABASE_URL') or 'sqlite:///./hr_system.db'


def get_sqlite_path(database_url: str) -> str:
    """Extract local sqlite path from a DATABASE_URL like sqlite:///./hr_system.db"""
    if not database_url.startswith("sqlite"):
        raise ValueError("Only sqlite URLs are supported by this helper")

    # Support sqlite:///relative/path or sqlite:////absolute/path
    prefix = "sqlite:///"
    if database_url.startswith(prefix):
        path = database_url[len(prefix):]
    else:
        # Fallback: remove sqlite: prefix
        path = database_url.split(":///")[-1]

    # If path is relative, make it relative to this file (backend folder)
    if not os.path.isabs(path):
        base_dir = os.path.dirname(__file__)
        path = os.path.abspath(os.path.join(base_dir, path))

    # If the computed path doesn't exist, also try resolving relative to the repository root
    if not os.path.exists(path):
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        alt = os.path.abspath(os.path.join(repo_root, os.path.relpath(path, start=base_dir)))
        if os.path.exists(alt):
            return alt

    return path


def column_exists(conn: sqlite3.Connection, table: str, column: str) -> bool:
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info('{table}')")
    rows = cur.fetchall()
    for r in rows:
        # PRAGMA returns: cid, name, type, notnull, dflt_value, pk
        if len(r) >= 2 and r[1] == column:
            return True
    return False


def add_column_sqlite(conn: sqlite3.Connection, table: str, column_def: str) -> None:
    cur = conn.cursor()
    sql = f"ALTER TABLE {table} ADD COLUMN {column_def}"
    cur.execute(sql)
    conn.commit()


def main():
    db_url = _get_database_url_from_env()
    try:
        sqlite_path = get_sqlite_path(db_url)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    if not os.path.exists(sqlite_path):
        print(f"[INFO] SQLite DB file does not exist at: {sqlite_path}")
        print("Nothing to do. If you want to (re)create the DB, run your create-tables or seed script.")
        return

    print(f"[INFO] Opening SQLite DB: {sqlite_path}")
    conn = sqlite3.connect(sqlite_path)

    try:
        if not column_exists(conn, 'goals', 'category_id'):
            print("[OK] 'category_id' column is missing in 'goals' table. Adding it now...")
            # Add the column without a foreign key constraint (SQLite limitations).
            add_column_sqlite(conn, 'goals', 'category_id INTEGER')
            print("[OK] Column 'category_id' added. Note: foreign key constraint not added (SQLite ALTER TABLE limitation).")
        else:
            print("[OK] 'category_id' column already exists in 'goals' table. No action needed.")

    except Exception as e:
        print(f"[ERROR] Failed to alter table: {e}")
    finally:
        conn.close()


if __name__ == '__main__':
    main()
