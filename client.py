import requests
import os
import subprocess
import sys

# Configuration
SECRET = os.environ.get("APP_SECRET") or "test"
REMOTE_URL = "https://downloader.atlantishq.com/get-list?secret=" + SECRET
REMOTE_URL = "http://localhost:5000/get-list?secret=" + SECRET

def fetch_json(remote_url):
    """
    Fetch JSON data from the remote URL using the provided token.
    """
    try:
        response = requests.get(remote_url, params={"secret": SECRET})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching JSON: {e}")
        sys.exit(1)

def execute_commands(urls):
    """
    Execute the command "echo $var" for each var in the provided list.
    """
    for var in urls:
        try:
            # Execute the command
            result = subprocess.run(
                ["echo", var],
                text=True,
                capture_output=True,
                check=True
            )
            # Print the command output
            print(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            print(f"Error executing command for {var}: {e}")

def main():
    # Fetch JSON data
    json_data = fetch_json(REMOTE_URL)

    # Extract "urls" key
    urls = json_data
    if not isinstance(urls, list):
        print("Invalid JSON structure: 'urls' key is not a list.")
        sys.exit(1)

    # Execute commands
    execute_commands(urls)

if __name__ == "__main__":
    main()
