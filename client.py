import requests
import subprocess
import sys

# Configuration
REMOTE_URL = "https://downloader.atlantishq.com/get-list"  # Replace with your actual URL
TOKEN = "secret"  # Replace with your actual token

def fetch_json(remote_url, token):
    """
    Fetch JSON data from the remote URL using the provided token.
    """
    try:
        response = requests.get(remote_url, params={"token": token})
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
    json_data = fetch_json(REMOTE_URL, TOKEN)

    # Extract "urls" key
    urls = json_data.get("urls", [])
    if not isinstance(urls, list):
        print("Invalid JSON structure: 'urls' key is not a list.")
        sys.exit(1)

    # Execute commands
    execute_commands(urls)

if __name__ == "__main__":
    main()
