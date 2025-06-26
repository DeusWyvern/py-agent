import os
from google.genai import types


def write_file(working_directory, file_path, content):
    abs_working = os.path.abspath(working_directory)
    if os.path.isabs(file_path):
        full_path = file_path
    else:
        full_path = os.path.abspath(os.path.join(abs_working, file_path))

    full_path_dir = os.path.dirname(full_path)

    if not full_path_dir.startswith(abs_working):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    elif not os.path.exists(full_path_dir):
        try:
            os.makedirs(full_path_dir)
        except Exception as e:
            return f"Error: cannot make directory(s) {e}"

    try:
        with open(full_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: cannot write to file. {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to the file at the file path relative to and constraied to the working directory. If the file and directories leading to the file don't exist, it will make them if able.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file.",
            ),
        },
    ),
)
