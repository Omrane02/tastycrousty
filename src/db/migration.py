from pathlib import Path

from sqlalchemy import text
from src.db.database import engine

MIGRATION_FILE =Path(__file__).parent / "migration.sql"

def run_migration() -> None:
    sql = MIGRATION_FILE.read_text(encoding="utf-8")
    with engine.begin() as conn:
        conn.execute(text(sql))