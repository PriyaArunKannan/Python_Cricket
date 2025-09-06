import os
import sqlite3
import pandas as pd
from transform import parse_matches  # re-use parser from transform.py
from transform import parse_batting
from transform import parse_bowling
from transform import build_team_results

DB_PATH = os.path.join(os.path.dirname(__file__), "cricket.db")

def save_to_db(df: pd.DataFrame, table_name: str):
    if df.empty:
        print(f"⚠️ Skipping {table_name}, no data.")
        return

    conn = sqlite3.connect(DB_PATH)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    print(f"✅ Saved {len(df)} rows to table: {table_name}")

if __name__ == "__main__":
    for fmt in ["odi", "t20", "test", "ipl"]:
        df = parse_matches(fmt)
        save_to_db(df, f"{fmt}_matches")
          
        df_batting = parse_batting(fmt)
        save_to_db(df_batting, f"batting_stats_{fmt}")

        df_bowling = parse_bowling(fmt)
        save_to_db(df_bowling, f"bowling_stats_{fmt}")

        df_team = build_team_results(fmt)
        save_to_db(df_team, f"team_results_{fmt}")
