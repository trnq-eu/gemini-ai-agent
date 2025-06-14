import os
import shutil
from pathlib import Path
from functions.run_python import run_python_file


if __name__ == "__main__":
    # Define the base directory for tests
    base_test_dir = Path("calculator")

    # Clean up before tests and create fresh directory
    if base_test_dir.exists():
        shutil.rmtree(base_test_dir)
    base_test_dir.mkdir(parents=True, exist_ok=True)

    # Create dummy files for testing
    with open(base_test_dir / "main.py", "w") as f:
        f.write('print("Ran main.py in calculator successfully")\n') # Modified to include "Ran"
        f.write('import sys\n')
        f.write('print(f"Running with args: {sys.argv}")\n')

    with open(base_test_dir / "tests.py", "w") as f: # This is a dummy file inside 'calculator'
        f.write('print("Hello from tests.py in calculator")\n')

    print("--- Test: run_python_file('calculator', 'main.py') ---")
    result1 = run_python_file(str(base_test_dir), "main.py")
    print(result1)
    print("-" * 20)

    print("--- Test: run_python_file('calculator', 'tests.py') ---")
    # Note: This 'tests.py' is the one we created inside the 'calculator' directory
    result2 = run_python_file(str(base_test_dir), "tests.py")
    print(result2)
    print("-" * 20)

    print("--- Test: run_python_file('calculator', '../main.py') (should be an error) ---")
    # This attempts to access a file outside the 'calculator' working directory.
    # The path '../main.py' relative to 'calculator' would resolve outside.
    result3 = run_python_file(str(base_test_dir), "../main.py")
    print(result3)
    print("-" * 20)

    print("--- Test: run_python_file('calculator', 'nonexistent.py') (should be an error) ---")
    result4 = run_python_file(str(base_test_dir), "nonexistent.py")
    print(result4)
    print("-" * 20)

    # Clean up test directory and files
    if base_test_dir.exists():
        shutil.rmtree(base_test_dir)