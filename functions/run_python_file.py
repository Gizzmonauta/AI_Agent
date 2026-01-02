import os
import subprocess
from google.genai import types 

# Build the function schema that tells the LLM how the function should be called.
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specified Python file relative to the working directory with optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to run, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional arguments to pass to the Python file (default is no arguments)",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        # Resolve absolute paths
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        # Validate the target file is within the working directory
        if not valid_target_file:
            raise Exception(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        
        # Check if the target file exists and is a file
        if not os.path.isfile(target_file):
            raise Exception(f'Error: "{file_path}" does not exist or is not a regular file') 
        
        # Check if the file has a .py extension
        if not target_file.endswith('.py'):
            raise Exception(f'Error: "{file_path}" is not a Python file')
        
        # Prepare the command to run the Python file
        command = ["python", target_file]
        if args is not None:
            command.extend(args)

        # Use subprocess to run the Python file and capture output
        result = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
        output_string = ""
        if result.returncode != 0:
            output_string += f"Process exited with code {result.returncode}\n"
        elif not result.stdout and not result.stderr:
            output_string += "No output produced" 
        else:
            output_string += f"STDOUT: {result.stdout}"
            output_string += "\n"
            output_string += f"STDERR: {result.stderr}"



    except Exception as e:
        return f"{e}"
    
    return output_string