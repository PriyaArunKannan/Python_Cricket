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

if __name__ == "__main__":
    for fmt in ["odi", "t20", "test", "ipl"]:
        df = parse_matches(fmt)
        print(f"\n{fmt.upper()} Matches Sample:")
        print(df.head())
