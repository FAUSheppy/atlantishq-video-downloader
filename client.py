import requests
import os
import subprocess
import sys
import random
import time

# Configuration
SECRET = os.environ.get("APP_SECRET") or "test"
HOST = os.environ.get("HOST") or "http://localhost:5000"
YT_DOWNLOADER_BIN = os.environ.get("YT_DOWNLOADER_BIN") or "/yt-dlp"
REMOTE_URL = HOST + "/get-list?secret=" + SECRET

def fetch_json(remote_url):

    try:
        response = requests.get(remote_url, params={"secret": SECRET})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching JSON: {e}")
        sys.exit(1)

def execute_commands(urls):

    for var in urls:
        if not var.replace("www.", "").startswith("https://youtube.com"):
            print("Refusing to do", var, "..because it is not a youtube.com url", file=sys.stderr)
            continue

        try:

            cmd = [ YT_DOWNLOADER_BIN, 
                        "-f", "bestvideo[height<=1080]+bestaudio/best",
                        "--sleep-interval", "10",
                        "--cache-dir", "./cache/",
                        "--rate-limit", "1200K",
                        "--max-sleep-interval", "20",
                        "--download-archive", "archive",
                        "--no-post-overwrites",
                        "--sponsorblock-remove", "sponsor,selfpromo,interaction,preview,filler,music_offtopic",
                        "--merge-output-format", "mkv",
                        "-o", '''%(uploader)s/%(title)s.%(ext)s''',
                        var,
            ]

            result = subprocess.run(cmd, text=True, capture_output=True, check=True)

            time.sleep(random.randint(10, 15))

        except subprocess.CalledProcessError as e:
            print(f"Error executing command for {var}: {e}")

def main():

    # get urls #
    json_data = fetch_json(REMOTE_URL)
    urls = json_data
    if not isinstance(urls, list):
        print("Invalid JSON structure: 'urls' key is not a list.")
        sys.exit(1)

    # execute commands #
    execute_commands(urls)

if __name__ == "__main__":

    main()
    time.sleep(random.randint(1,5))

