import os

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
        
        # Security check: abs_file_path must be within abs_working_dir.
        # It's outside if it's not the same path and doesn't start with abs_working_dir + path separator.
        prefix_to_check = abs_working_dir.rstrip(os.sep) + os.sep
   
         # A file path is considered "inside" if it's the working directory itself (though unlikely for a file)
        # or if it starts with the working directory's path followed by a separator.
        is_same_as_working_dir = (abs_file_path == abs_working_dir)
        is_subdir_of_working_dir = abs_file_path.startswith(prefix_to_check)


        if not (is_same_as_working_dir or is_subdir_of_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        try:
            with open(abs_file_path, "r", encoding='utf-8') as f:
                content = f.read(MAX_CHARS + 1)

            if len(content) > MAX_CHARS:
                    return content[:MAX_CHARS] + f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content
        except OSError as e:
            return f"Error: Could not read file \"{file_path}\": {e.strerror}"
        except UnicodeDecodeError:
            # This can happen if the file is binary or not UTF-8 encoded
            return f"Error: Could not decode file \"{file_path}\" as UTF-8. It may be a binary file or use a different text encoding."
    except Exception as e:
        # Catch-all for other unexpected errors during path resolution or other operations
        return f"Error: An unexpected error occurred while processing \"{file_path}\": {str(e)}"