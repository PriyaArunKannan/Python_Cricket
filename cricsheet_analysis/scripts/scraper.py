import os
import requests
import zipfile

DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "../data")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

ZIP_LINKS = {
    "odi": "https://cricsheet.org/downloads/odis_json.zip",
    "t20": "https://cricsheet.org/downloads/t20s_json.zip",
    "test": "https://cricsheet.org/downloads/tests_json.zip",
    "ipl": "https://cricsheet.org/downloads/ipl_json.zip"
}

def download_and_extract():
    for match_type, url in ZIP_LINKS.items():
        zip_path = os.path.join(DOWNLOAD_DIR, f"{match_type}.zip")
        extract_path = os.path.join(DOWNLOAD_DIR, match_type)

        if not os.path.exists(extract_path):
            print(f"Downloading {match_type} data...")
            r = requests.get(url, stream=True)
            with open(zip_path, "wb") as f:
                f.write(r.content)

            print(f"Extracting {match_type} data...")
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_path)

            os.remove(zip_path)  # cleanup
        else:
            print(f"{match_type} data already downloaded.")

if __name__ == "__main__":
    download_and_extract()
