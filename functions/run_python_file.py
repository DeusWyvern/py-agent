import os
import subprocess


def run_python_file(working_directory, file_path):
    abs_working = os.path.abspath(working_directory)
    if os.path.isabs(file_path):
        full_path = file_path
    else:
        full_path = os.path.abspath(os.path.join(abs_working, file_path))

    if not full_path.startswith(abs_working):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    elif not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            ["python3", full_path],
            timeout=30,
            capture_output=True,
            text=True,
            cwd=abs_working,
        )

        std_output = []
        if result.stdout:
            std_output.append(f"STDOUT: \n{result.stdout}")
        if result.stderr:
            std_output.append(f"STDERR: \n{result.stderr}")
        if result.returncode != 0:
            std_output.append(f"Process exited with code {result.returncode}")

        return "\n".join(std_output) if std_output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"
