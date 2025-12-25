import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working_directory = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not target_file.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'Error: File "{file_path}" not found.'
    
    if not target_file.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        args = [args]
        path = os.path.join(working_directory, file_path)
        more_args = ["python", path]
        args = more_args + args
        completed_process = subprocess.run(args=args, timeout=30, capture_output=True)
        if completed_process.returncode != 0:
            return f"Process exited with code {completed_process.returncode}"
        
        if completed_process.stdout is None:
            return "No output produced."
        string = f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}"
        return string
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute the python file in the specified file_path along with its optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to search files from.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file_path in which the file resides to execute."
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Optional Arguments for executing the python file"
            )
        },
    ),
)
     