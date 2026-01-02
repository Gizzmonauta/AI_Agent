import os
from google.genai import types 

# Build the function schema that tells the LLM how the function should be called.
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write content to, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the specified file",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        # Resolve absolute paths
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        # Validate the target file is within the working directory
        if not valid_target_file:
            raise Exception(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        
        # Check if the file path points to a directory not a file
        if os.path.isdir(target_file):
            raise Exception(f'Error: Cannot write to "{file_path}" as it is a directory') 
        
        # Get the target directory
        target_dir = os.path.dirname(target_file)

        # Create directories if they do not exist
        os.makedirs(target_dir, exist_ok=True)

        # Write content to the file
        with open(target_file, "w") as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return str(e)