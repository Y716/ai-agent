import os
from config import CHAR_LIMIT
from google.genai import types

def get_file_content(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not target_file.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'    
    try:  
        with open(target_file, 'r') as f:
            file_contents = f.read(CHAR_LIMIT)
            return file_contents
    except Exception as e:
        return f"Error listing files{e}"
    
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Return the contents of an existing file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to search files from.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file_path in which the file resides."
            )
        },
    ),
)