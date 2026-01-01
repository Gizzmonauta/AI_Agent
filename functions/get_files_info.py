import os

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
            print(f"Processing file: {filename}")
            file_size = os.path.getsize(filename)
            is_dir = os.path.isdir(filename)
            results.append(f"- {filename}: file_size={file_size}, is_directory={is_dir}")
        return "\n".join(results)

    except Exception as e:
        return str(e)

get_files_info("./calculator", "pkg")
get_files_info("./calculator", "./function")
get_files_info("./calculator", "../../function")
