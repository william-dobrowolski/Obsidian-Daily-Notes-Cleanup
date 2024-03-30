# Cleanup Empty Obsidian Daily Notes

This script is designed to help manage unused Markdown files created by the Daily Notes core Obsidian plugin. It finds and deletes empty (0B) Markdown files. It utilizes a `.env` file to securely store the location of the Obsidian vault and logs all actions for accountability and traceability.

## Features

- Load Obsidian vault location from an environment variable.
- Confirm the presence of the `daily-notes.json` settings file within the `.obsidian` directory.
- Recursively search for and delete empty Markdown files within the specified daily notes folder.

## Prerequisites

- Python 3.6 or later.
- A `.env` file with a `vault_location` variable set to the path of your Obsidian vault. The program will prompt for a vault location if this is not provided.

## Usage

1. Clone the repository to your local machine.
2. Ensure you have a `.env` file in the root directory with the following content (update the path to match your setup):

    ```
    vault_location=/path/to/your/obsidian/vault
    ```

3. Run the script:

    ```bash
    python md_cleanup.py
    ```

4. Check `md_cleanup_log.log` for a log of deleted files or any errors encountered.

## Contributing

Contributions are welcome! If you have suggestions for improvements or bug fixes, please open an issue or a pull request.

