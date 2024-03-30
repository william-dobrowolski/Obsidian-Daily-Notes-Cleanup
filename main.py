# Will Dobrowolski

import os
import json
import sys
from dotenv import load_dotenv, find_dotenv, set_key
from pathlib import Path

def load_env():
    '''
    Checks for an .env file. Prompts user for location if an .env file with a "vault_location" isn't found.
    '''
    # Try to load the .env file
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path=dotenv_path)

    # Check if the "vault_location" is set
    vault_location = os.environ.get("vault_location")

    if not vault_location:
        # Prompt the user for a "vault location" if it isn't found in the .env
        vault_location = input("Please provide a vault_location value: ")

        # If the .env file exists
        if dotenv_path:
            set_key(dotenv_path, "vault_location", vault_location)
        # Otherwise, create one in the root folder of the script
        else:
            dotenv_path = '.env'
            with open(dotenv_path, "w") as file:
                file.write(f"vault_location={vault_location}\n")
        
        # Load the newly set environment variable
        os.environ["vault_location"] = vault_location

    return vault_location
    print(f"Vault location: {vault_location}")


def confirm_vault_location(vault_location):
    '''
    Confirms that the vault_location loaded from environment contains "daily-notes.json"
    '''
    # Create a Path object
    vault_path = Path(vault_location)

    # Check if the path exists and is a directory
    if vault_path.exists() and vault_path.is_dir():
        # Search for "daily-notes.json" file
        notes_settings = vault_path / ".obsidian" / "daily-notes.json"

        if notes_settings.exists() and notes_settings.is_file():
            print(f"The daily notes settings were found in: {notes_settings}")
            daily_notes_path = Path(notes_settings)
            return daily_notes_path
        else:
            print(f"Did not find daily notes settings in the specified vault location")
            return None
    else:
        print("The specified vault location does not exist or is not a directory.")
        return None

def load_json_file(json_file_path):
    '''
    Returns a dictionary from a specified JSON
    '''
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data

def main():
    vault_location = load_env()
    daily_notes_location = confirm_vault_location(vault_location)

    # Exits program if no daily-notes found
    if not confirm_vault_location:
        sys.exit("Cannot proceed without valid 'daily-notes.json' file.")

    print(f"Daily Notes settings are in: {daily_notes_location}")

    daily_notes_data = load_json_file(daily_notes_location)
    daily_vault_location = daily_notes_data["folder"]

    print(daily_notes_data)
    print(f"Daily notes location in vault: {daily_vault_location}")

if __name__ == "__main__":
    main()