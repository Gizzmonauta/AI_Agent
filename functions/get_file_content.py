import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        # Resolve absolute paths
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        # Validate the target file is within the working directory
        if not valid_target_file:
            raise Exception(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        
        # Check if the target file exists and is a file
        if not os.path.isfile(target_file):
            raise Exception(f'Error: File not found or is not a regular file: "{file_path}"') 

        # Read the file content up to MAX_CHARS
        with open(target_file, 'r') as f:
            content = f.read(MAX_CHARS)
        
            # After reading the first MAX_CHARS...
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'


    except Exception as e:
        return str(e)
    
    return content

