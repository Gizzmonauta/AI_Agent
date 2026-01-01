import os
from functions.get_file_content import *
from config import MAX_CHARS

def test_get_file_content(wd, d):
    result = get_file_content(wd, d)
    if d == "lorem.txt":
        print(f"Result for '{d}' directory is too long, length: {len(result)}")
        if "[...File " in result:
            print(f"Truncation notice found in result.\n")
        else:
            print(f"Truncation notice NOT found in result.\n")
    elif d == ".":
        print(f"Result for current directory:\n{result}\n")
    else:    
        print(f"Result for '{d}' directory:\n{result}\n")

# Example test cases
test_get_file_content("calculator", "lorem.txt")
test_get_file_content("calculator", "main.py")
test_get_file_content("calculator", "pkg/calculator.py")
test_get_file_content("calculator", "/bin/cat") # this should return an error string
test_get_file_content("calculator", "pkg/does_not_exist.py") # this should return an error string