import os
from functions.get_files_info import *

def test_get_files_info(wd, d):
    result = get_files_info(wd, d)
    if d == ".":
        print(f"Result for current directory:\n{result}\n")
    else:    
        print(f"Result for '{d}' directory:\n{result}\n")

# Example test cases
test_get_files_info("calculator", ".")
test_get_files_info("calculator", "pkg")
test_get_files_info("calculator", "/bin")
test_get_files_info("calculator", "../")