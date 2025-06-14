import os
import subprocess
from pathlib import Path # pathlib often makes path manipulation more intuitive

def run_python_file(working_directory, file_path):
    try:
        # Convert to Path objects for easier manipulation and robustness
        abs_working_dir_path = Path(working_directory).resolve() # .resolve() gets absolute, canonical path

        # Create the full file path by joining and then resolving
        # .resolve() will handle '..' components and give the true absolute path
        abs_file_path_resolved = (abs_working_dir_path / file_path).resolve()

        # Ensure the file path is within the working directory (robust check)
        # Check if the resolved file path starts with the resolved working directory path
        # AND check that the path components of the file are genuinely within the working dir.
        # This is often done by checking if abs_file_path_resolved is "descendant" of abs_working_dir_path
        # A simple string startswith on resolved paths is usually robust enough,
        # but let's confirm the current logic is correct for this specific problem.
        
        # Simpler and often sufficient check:
        # if not str(abs_file_path_resolved).startswith(str(abs_working_dir_path)):
        #     return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # More robust check using Pathlib's relative_to (Python 3.5+)
        try:
            # If the file path can be made relative to the working directory, it's inside.
            # If it cannot (e.g., it's outside), a ValueError is raised.
            abs_file_path_resolved.relative_to(abs_working_dir_path)
        except ValueError:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'


        # Convert back to string for os.path functions if needed, or continue with Path objects
        abs_file_path_str = str(abs_file_path_resolved)
        abs_working_dir_str = str(abs_working_dir_path) # Use the resolved working directory for cwd

        # Check if the file exists
        if not os.path.exists(abs_file_path_str):
            return f'Error: File "{file_path}" not found.'

        if not abs_file_path_str.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        
        try:
            result = subprocess.run(
                ['python', abs_file_path_str], # Use the string representation for subprocess
                cwd = abs_working_dir_str,     # Use the resolved string path for cwd
                timeout = 30,
                capture_output=True,
                text=True,
                check=False
            )

            output_parts = []

            if result.stdout:
                output_parts.append(f"STDOUT:\n{result.stdout.strip()}")

            if result.stderr:
                output_parts.append(f"STDERR:\n{result.stderr.strip()}")

            if result.returncode != 0:
                output_parts.append(f"Process exited with code {result.returncode}")

            if not output_parts:
                return "No output produced."
            else:
                return "\n".join(output_parts)
            
        except subprocess.TimeoutExpired as e:
            output_parts = []
            if e.stdout:
                output_parts.append(f"STDOUT:\n{e.stdout.strip()}")
            if e.stderr:
                output_parts.append(f"STDERR:\n{e.stderr.strip()}")
            
            output_parts.append("Error: Python file execution timed out after 30 seconds.")
            return "\n".join(output_parts)

        except FileNotFoundError:
            return "Error: Python interpreter not found. Ensure Python is installed and in your system's PATH."
        except Exception as e:
            return f"Error: executing Python file: {e}"

    except Exception as e:
        return f"Error: during file path processing: {e}"