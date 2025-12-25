import os
from google.genai import types

def write_file(working_directory, file_path, contents):
    abs_working_directory = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not target_file.startswith(abs_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        with open(target_file, 'w') as f:
            f.write(contents)
            return f'Successfully wrote to "{file_path}" ({len(contents)} characters written)'
    except Exception as e:
        return f"Error listing files{e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or Overwrite the file in the specified file_path with the contents that are given, constrained to the working directory.",
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
            ),
            "contents": types.Schema(
                type=types.Type.STRING,
                description="Contents to write in the file"
            )
        },
    ),
)