import os
from google.genai import types


def get_file_content(working_directory, file_path):
    abs_working = os.path.abspath(working_directory)
    if os.path.isabs(file_path):
        full_path = file_path
    else:
        full_path = os.path.abspath(os.path.join(abs_working, file_path))

    if not full_path.startswith(abs_working):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(full_path):
        return f'Error: "{file_path}" is not a file'

    try:
        MAX_CHARS = 10000

        with open(full_path) as f:
            file_content_string = f.read(MAX_CHARS)
            if len(f.read()) > MAX_CHARS:
                file_content_string = (
                    file_content_string
                    + f'[File "{full_path}" truncated at 10000 characters]'
                )
            return file_content_string

    except Exception as e:
        return f"Error: Could not read file. {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the content of the specified file truncated to a maximum of 10k characters. File locations constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory.",
            ),
        },
    ),
)
