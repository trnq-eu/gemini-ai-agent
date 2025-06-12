from functions.get_files_info import get_files_info
import os

if __name__ == "__main__":
    # Note: The output of these tests will depend on whether "calculator"
    # and "calculator/pkg" exist and are accessible in the current working directory
    # when tests.py is executed. The function is designed to return error strings
    # for non-existent or inaccessible paths.

    print("--- Test: get_files_info('calculator', '.') ---")
    # If 'calculator' dir exists at the execution location of tests.py: lists contents of 'calculator'
    # Otherwise: 'Error: Working directory "calculator" is not a directory.' or similar.
    result1 = get_files_info("calculator", ".")
    print(result1)
    print("-" * 20)

    print("--- Test: get_files_info('calculator', 'pkg') ---")
    # If 'calculator/pkg' exists: lists contents of 'calculator/pkg'
    # Otherwise: 'Error: "pkg" is not a directory' or 'Error: Working directory "calculator" is not a directory.'
    result2 = get_files_info("calculator", "pkg")
    print(result2)
    print("-" * 20)

    print("--- Test: get_files_info('calculator', '/bin') ---")
    result3 = get_files_info("calculator", "/bin") # Should be an error
    print(result3)
    print("-" * 20)

    print("--- Test: get_files_info('calculator', '../') ---")
    result4 = get_files_info("calculator", "../") # Should be an error
    print(result4)
    print("-" * 20)