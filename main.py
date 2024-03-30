# Will Dobrowolski

import os
import json
import sys
import logging
from dotenv import load_dotenv, find_dotenv, set_key
from pathlib import Path

logging.basicConfig(filename='md_cleanup_log.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

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
            # print(f"The daily notes settings were found in: {notes_settings}")
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

def find_mds(vault_path):
    '''
    Recursively search the daily notes location for .md files that are 0KB.
    Return as list of Path objects.
    '''
    vault_path = Path(vault_path)

    md_files_zero_kb = [file for file in vault_path.glob("**/*.md") if file.stat().st_size == 0]

    return md_files_zero_kb

def delete_md_files(files_to_delete):
    '''
    Deletes each .md file in the provided list of Path objects
    '''
    for file_path in files_to_delete:
        try:
            file_path.unlink()
            logging.info(f"Deleted: {file_path}")
            print(f"Deleted: {file_path}")
        except FileNotFoundError:
            logging.warning(f"File not found: {file_path}")
            print(f"File not found {file_path}")
        except Exception as e:
            logging.error(f"Error deleting {file_path}: {e}")
            print(f"Error deleting {file_path}: {e}")


def main():
    vault_path = Path(load_env())
    print(f"Vault Path: {vault_path}")
    
    daily_notes_settings_path = confirm_vault_location(vault_path)
    print(f"Daily Notes Settings Path: {daily_notes_settings_path}")

    # Exits program if no daily-notes found
    if not confirm_vault_location(vault_path):
        sys.exit("Cannot proceed without valid 'daily-notes.json' file.")

    daily_notes_settings = load_json_file(daily_notes_settings_path)
    print(f"Daily Notes Settings: {daily_notes_settings}")

    daily_notes_folder = daily_notes_settings["folder"]
    print(f"Daily Notes Folder: {daily_notes_folder}")

    daily_notes_folder_path = Path(vault_path / f"{daily_notes_folder}")
    print(f"Daily Notes folder path: {daily_notes_folder_path}")

    empty_md_files = find_mds(daily_notes_folder_path)
    print(empty_md_files)

    delete_md_files(empty_md_files)

if __name__ == "__main__":
    main()