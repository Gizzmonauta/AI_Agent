import os
from functions.run_python_file import *

def test_run_python_file(wd, fp, args=None):
    result = run_python_file(wd, fp, args)
    if fp == ".":
        print(f"Result for current directory:\n{result}\n")
    else:    
        print(f"Result for '{fp}' directory:\n{result}\n")

# Example test cases
test_run_python_file("calculator", "main.py") # (should print the calculator's usage instructions)
test_run_python_file("calculator", "main.py", ["3 + 5"]) # (should run the calculator... which gives a kinda nasty rendered result)
test_run_python_file("calculator", "tests.py") # (should run the calculator's tests successfully)
test_run_python_file("calculator", "../main.py") # (this should return an error)
test_run_python_file("calculator", "nonexistent.py") # (this should return an error)
test_run_python_file("calculator", "lorem.txt") # (this should return an error)