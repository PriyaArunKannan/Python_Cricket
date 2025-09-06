import sqlite3
import pandas as pd
import os

def build_batting_summary(fmt: str):
    conn = sqlite3.connect("cricket.db")
    query = f"""
    CREATE TABLE IF NOT EXISTS batting_stats_{fmt} AS
    SELECT 
        batsman AS batter,
        SUM(runs_batsman) AS runs,
        COUNT(*) AS balls,
        SUM(CASE WHEN runs_batsman = 4 THEN 1 ELSE 0 END) AS fours,
        SUM(CASE WHEN runs_batsman = 6 THEN 1 ELSE 0 END) AS sixes,
        ROUND(CAST(SUM(runs_batsman) AS FLOAT) / COUNT(*) * 100, 2) AS strike_rate
    FROM deliveries_{fmt}
    GROUP BY batsman;
    """
    conn.execute(query)
    conn.commit()
    conn.close()

DB_PATH = os.environ.get("CRICSHEET_DB", "scripts/cricket.db")

def get_tables():
    """
    Retrieve a sorted list of table names in the SQLite database.
    
    Returns:
        list: Sorted list of table names.
    """
    print(f"DB path - {DB_PATH}")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"⚠️ Tables found: {tables}")
        return sorted(tables)

def table_exists(table_name):
    """
    Check if a table exists in the SQLite database.
    
    Args:
        table_name (str): Name of the table to check.
    
    Returns:
        bool: True if the table exists, False otherwise.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,)
        )
        return cursor.fetchone()[0] > 0

if __name__ == "__main__":
   get_tables()
