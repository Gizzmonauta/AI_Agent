from functions.write_file import *
import os

def test_write_file(wd, fn, c):
    result = write_file(wd, fn, c)
    if fn == ".":
        print(f"Result for current directory:\n{result}\n")
    else:    
        print(f"Result for '{fn}' directory:\n{result}\n")

# Example test cases
test_write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
test_write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
test_write_file("calculator", "/tmp/temp.txt", "this should not be allowed")