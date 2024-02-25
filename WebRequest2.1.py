import subprocess
import os
import configparser
import requests

def download_file(url, output_filepath):
    """Downloads a file using either PowerShell or requests, handling errors."""

    try:
        # Attempt download using PowerShell first
        powershell_command = f'Invoke-WebRequest -Uri "{url}" -OutFile "{output_filepath}"'
        subprocess.run(['powershell', '-Command', powershell_command])
    except subprocess.CalledProcessError as e:
        print(f"PowerShell download failed: {e}")

        # If PowerShell fails, fall back to requests
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for error status codes

            with open(output_filepath, 'wb') as f:
                f.write(response.content)

        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")
        except requests.exceptions.Timeout as e:
            print(f"Request to {url} timed out: {e}")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error for {url}: {e.response.status_code} - {e.response.text}")

def get_config_values(config_filepath):
    """Reads values from a configuration file."""
    config = configparser.ConfigParser()
    config.read(config_filepath)
    return config['DEFAULT']  # Assuming a 'DEFAULT' section in the config

if __name__ == "__main__":
    default_config_filepath = 'config.ini'  # Default location
    config_filepath = os.path.expanduser('~/path/to/your/config.ini')  # Modify this!

    try:
        config = get_config_values(config_filepath)
    except FileNotFoundError:
        print(f"Configuration file not found at: {config_filepath}. Using defaults.")
        config = get_config_values(default_config_filepath)  # Fallback to default

    target_url = config.get('target_url')  # Use .get() to provide a default
    if target_url is None:
        print("Error: 'target_url' is missing in the configuration. Please check your settings.")
        exit()  # Or provide a default URL here

    output_directory = config['output_directory']
    output_filename = 'downloaded_file.html'
    output_filepath = os.path.join(output_directory, output_filename)

    download_file(target_url, output_filepath)