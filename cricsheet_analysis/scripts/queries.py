import sqlite3
import pandas as pd

DB_PATH = "cricket.db"

def run_query(query: str):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

if __name__ == "__main__":
    queries = {
        # 1. Total matches per format
        "matches_per_format": """
            SELECT 'ODI' AS format, COUNT(*) AS matches FROM odi_matches
            UNION ALL
            SELECT 'T20', COUNT(*) FROM t20_matches
            UNION ALL
            SELECT 'Test', COUNT(*) FROM test_matches;
        """,

        # 2. Top 10 venues by matches played (ODI example)
        "top_venues_odi": """
            SELECT venue, COUNT(*) AS matches
            FROM odi_matches
            GROUP BY venue
            ORDER BY matches DESC
            LIMIT 10;
        """,

        # 3. Toss winner vs match winner (T20 example)
        "toss_vs_winner_t20": """
            SELECT
                CASE WHEN toss_winner = match_winner  THEN 'Toss=Match Winner'
                     ELSE 'Toss≠Match Winner' END AS outcome,
                COUNT(*) AS count
            FROM t20_matches
            GROUP BY outcome;
        """,

        # 4. Matches per year (Test)
        "matches_per_year_test": """
            SELECT  SUBSTR(date, 1, 4) AS season, COUNT(*) AS matches
            FROM test_matches
            GROUP BY season
            ORDER BY season;
        """,

        # 5. Most common result type in ODIs
        "odi_result_type": """
            SELECT  match_winner AS result, COUNT(*) AS count
            FROM odi_matches
            GROUP BY result
            ORDER BY count DESC;
        """
    }

    for name, query in queries.items():
        print(f"\n▶️ {name}")
        df = run_query(query)
        print(df.head())
