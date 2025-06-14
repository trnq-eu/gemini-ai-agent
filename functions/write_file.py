import os
from pathlib import Path

def write_file(working_directory: str, file_path: str, content: str) -> str:
    """
    Writes content to a file, ensuring it's within the working_directory.
    Creates the file and any necessary parent directories if they don't exist.
    Overwrites the file if it already exists.
    """
    # Store the path string for error messages, defaulting to the input file_path
    path_for_error_msg = file_path
    try:
        # get absolute working directory
        abs_working_dir = os.path.abspath(working_directory)

        # create the full file path relative to the absolute working directory
        abs_file_path = os.path.join(abs_working_dir, file_path)


        # ensure the file path is within the working directory
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Ensure the directory exists before writing the file
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)

        # Write the content to the file, overwriting existing content
        with open(abs_file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    

    except OSError as e:
        # Catch OS-related errors (e.g., permission denied, invalid path)
        return f"Error: Failed to write to '{file_path}': {e}"
    except Exception as e:
        # Catch any other unexpected errors
        return f"Error: An unexpected error occurred while writing to '{file_path}': {e}"