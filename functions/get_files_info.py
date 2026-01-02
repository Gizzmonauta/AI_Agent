import os
from google.genai import types 

# Build the function schema that tells the LLM how the function should be called.
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
    
        # Resolve absolute paths
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        # Validate the target directory is within the working directory
        if not valid_target_dir:
            raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        
        # Check if the target directory exists and is a directory
        if not os.path.isdir(target_dir):
            raise Exception(f'Error: "{directory}" is not a directory') 

        # List files in the target directory
        list_of_files = os.listdir(target_dir)
        results = []
        for filename in list_of_files:
            full_path = os.path.join(target_dir, filename)
            file_size = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)
            results.append(f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(results)

    except Exception as e:
        return str(e)
