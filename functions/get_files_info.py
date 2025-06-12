import os

def get_files_info(working_directory, directory=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)

        if directory is None:
            # Target directory is the working directory itself
            path_to_list = abs_working_dir
        else:
            # Resolve the target directory path.
            # os.path.join handles 'directory' being absolute (e.g., "/bin")
            # or relative (e.g., "subdir", "../").
            path_to_list = os.path.abspath(os.path.join(abs_working_dir, directory))

            # Security check: path_to_list must be abs_working_dir or a subdirectory of it.
            # It's outside if it's not the same path and doesn't start with abs_working_dir + path separator.
            # Normalizing abs_working_dir to ensure it ends with a separator for the startswith check,
            # unless it's the root directory.
            # Example: abs_working_dir = /foo/bar -> check prefix /foo/bar/
            # Example: abs_working_dir = / -> check prefix /
            prefix_to_check = abs_working_dir.rstrip(os.sep) + os.sep
            if not (path_to_list == abs_working_dir or path_to_list.startswith(prefix_to_check)):
                return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if path_to_list is a directory
        if not os.path.isdir(path_to_list):
            if directory is None:
                # This means working_directory itself (resolved to path_to_list) is not a directory
                return f'Error: Working directory "{working_directory}" is not a directory.'
            else:
                # This means the 'directory' argument (resolved to path_to_list) is not a directory
                return f'Error: "{directory}" is not a directory'

        output_lines = []
        try:
            listed_item_names = os.listdir(path_to_list)
        except OSError as e:
            return f"Error: Could not list directory contents for \"{path_to_list}\": {e.strerror}"

        for name in listed_item_names:
            item_path = os.path.join(path_to_list, name)
            try:
                is_dir = os.path.isdir(item_path)
                # os.path.getsize follows symlinks. Raises OSError for broken symlinks or inaccessible files.
                file_size = os.path.getsize(item_path)
                output_lines.append(f"- {name}: file_size={file_size} bytes, is_dir={is_dir}")
            except OSError as e:
                # If an error occurs for any item, the whole function should return an error string
                # as per the requirement "catch them and instead return a string describing the error".
                return f"Error: Failed to get info for item \"{name}\" in \"{path_to_list}\": {e.strerror}"
        
        if not output_lines and not listed_item_names: # Directory is empty
            return f"Directory '{path_to_list}' is empty."
        return "\n".join(output_lines)

    except Exception as e:
        # Catch-all for other unexpected errors
        return f"Error: An unexpected error occurred: {str(e)}"
