import os
import pandas as pd
import json

BASE_DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")

def load_json_files(format_folder):
    folder_path = os.path.join(BASE_DATA_DIR, format_folder)
    all_matches = []
    if not os.path.exists(folder_path):
        print(f"No folder found for {format_folder}")
        return all_matches

    for file in os.listdir(folder_path):
        if file.endswith(".json"):
            with open(os.path.join(folder_path, file), "r", encoding="utf-8") as f:
                data = json.load(f)
                all_matches.append(data)
    return all_matches

def parse_matches(match_format):
    matches = load_json_files(match_format)
    match_list = []

    for m in matches:
        meta = m.get("info", {})
        match_list.append({
            "match_id": m.get("meta", {}).get("data_version"),
            "format": meta.get("match_type"),
            "teams": str(meta.get("teams")),
            "venue": meta.get("venue"),
            "date": meta.get("dates", [None])[0],
            "toss_winner": meta.get("toss", {}).get("winner"),
            "match_winner": meta.get("outcome", {}).get("winner")
        })


    return pd.DataFrame(match_list)

def parse_batting1(match_format):
    matches = load_json_files(match_format)
    batting_rows = []

    for m in matches:
        match_id = m.get("meta", {}).get("data_version")
        innings = m.get("innings", [])

        for inn in innings:
            for team, details in inn.items():
                deliveries = details.get("deliveries", [])
                for d in deliveries:
                    for ball, info in d.items():
                        batter = info.get("batsman")
                        runs = info.get("runs", {}).get("batsman", 0)

                        batting_rows.append({
                            "match_id": match_id,
                            "team": team,
                            "batter": batter,
                            "runs": runs,
                            "ball": ball
                        })

    return pd.DataFrame(batting_rows)

def parse_batting(fmt: str):
    matches = load_json_files(fmt)
    batting_records = []

    for m in matches:
        innings = m.get("innings", [])
        for inning in innings:
            team = inning.get("team")
            overs = inning.get("overs", [])
            for over in overs:
                for ball in over.get("deliveries", []):
                    batter = ball.get("batter")
                    runs = ball.get("runs", {}).get("batter", 0)

                    batting_records.append({
                        "match_id": m.get("meta", {}).get("match_id"),
                        "team": team,
                        "batter": batter,
                        "runs": runs,
                        "ball": 1,
                        "four": 1 if runs == 4 else 0,
                        "six": 1 if runs == 6 else 0
                    })

    df = pd.DataFrame(batting_records)
    if df.empty:
        return df

    summary = (
        df.groupby(["batter", "team"])
        .agg({
            "runs": "sum",
            "ball": "count",
            "four": "sum",
            "six": "sum"
        })
        .reset_index()
    )
    summary["strike_rate"] = round(summary["runs"] / summary["ball"] * 100, 2)
    return summary

import pandas as pd

def parse_bowling(fmt: str):
    matches = load_json_files(fmt)
    bowling_records = []

    for m in matches:
        innings = m.get("innings", [])
        for inning in innings:
            team = inning.get("team")   # bowling against this team
            overs = inning.get("overs", [])
            for over in overs:
                for ball in over.get("deliveries", []):
                    bowler = ball.get("bowler")
                    runs = ball.get("runs", {}).get("total", 0)
                    extras = ball.get("runs", {}).get("extras", 0)
                    legal_delivery = 0 if extras > 0 and "wides" in ball.get("extras", {}) else 1
                    wicket = 1 if "wickets" in ball else 0

                    bowling_records.append({
                        "match_id": m.get("meta", {}).get("match_id"),
                        "bowler": bowler,
                        "against_team": team,
                        "runs_conceded": runs,
                        "ball": legal_delivery,   # only legal balls count
                        "wicket": wicket
                    })

    df = pd.DataFrame(bowling_records)
    if df.empty:
        return df

    # aggregate
    summary = (
        df.groupby(["bowler", "against_team"])
        .agg({
            "runs_conceded": "sum",
            "ball": "sum",
            "wicket": "sum"
        })
        .reset_index()
    )

    # derived stats
    summary["overs"] = summary["ball"] // 6 + (summary["ball"] % 6) / 10
    summary["economy"] = round(summary["runs_conceded"] / (summary["ball"] / 6), 2)
    summary["strike_rate"] = summary.apply(
        lambda x: round(x["ball"] / x["wicket"], 2) if x["wicket"] > 0 else None, axis=1
    )
    summary["avg"] = summary.apply(
        lambda x: round(x["runs_conceded"] / x["wicket"], 2) if x["wicket"] > 0 else None, axis=1
    )

    return summary


def parse_bowling2(match_format):
    matches = load_json_files(match_format)
    bowling_rows = []

    for m in matches:
        match_id = m.get("meta", {}).get("data_version")
        innings = m.get("innings", [])

        for inn in innings:
            for team, details in inn.items():
                deliveries = details.get("deliveries", [])
                for d in deliveries:
                    for ball, info in d.items():
                        bowler = info.get("bowler")
                        runs = info.get("runs", {}).get("total", 0)
                        extras = info.get("runs", {}).get("extras", 0)
                        wicket = 1 if "wicket" in info else 0

                        bowling_rows.append({
                            "match_id": match_id,
                            "team": team,
                            "bowler": bowler,
                            "runs_conceded": runs,
                            "extras": extras,
                            "wicket": wicket,
                            "ball": ball
                        })

    return pd.DataFrame(bowling_rows)

# import sqlite3
# import pandas as pd
# from utils import load_json_files   # assuming you already have this

# DB_PATH = "cricket.db"

def build_team_results(fmt: str) -> pd.DataFrame:
    matches = load_json_files(fmt)   # loads all JSON files for this format
    team_stats = {}

    for m in matches:
        info = m.get("info", {})
        teams = info.get("teams", [])
        winner = info.get("outcome", {}).get("winner")

        for team in teams:
            if team not in team_stats:
                team_stats[team] = {"matches": 0, "wins": 0, "losses": 0}

            team_stats[team]["matches"] += 1
            if team == winner:
                team_stats[team]["wins"] += 1
            else:
                team_stats[team]["losses"] += 1

    # convert dict → DataFrame
    df = pd.DataFrame([
        {"team": team,
         "matches": stats["matches"],
         "wins": stats["wins"],
         "losses": stats["losses"],
         "win_percent": round(stats["wins"] * 100 / stats["matches"], 2)
        }
        for team, stats in team_stats.items()
    ])

    return df


if __name__ == "__main__":
    for fmt in ["odi", "t20", "test", "ipl"]:
        # df = parse_matches(fmt)
        # print(f"\n{fmt.upper()} Matches Sample:")
        # print(df.head())

        df1 = parse_bowling(fmt)
        print(f"\n{fmt.upper()} Matches Sample:")
        print(df1.head())

        
