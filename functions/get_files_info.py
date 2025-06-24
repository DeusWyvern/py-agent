import os


def get_files_info(working_directory, directory=None):
    try:
        if directory is None:
            directory = "."

        abs_working = os.path.abspath(working_directory)
        if os.path.isabs(directory):
            full_path = directory
        else:
            full_path = os.path.abspath(os.path.join(abs_working, directory))

        if not full_path.startswith(abs_working):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'

        file_list = os.listdir(full_path)
        size_list = list(map(lambda x: get_path_size(x, full_path), file_list))
        return "\n".join(size_list)
    except Exception as e:
        return f"Error encountered listing files: {e}"


def get_path_size(file, path):
    file_path = os.path.join(path, file)
    file_size = os.path.getsize(file_path)
    file_is_dir = os.path.isdir(file_path)
    return f"- {file}: file_size={file_size} bytes, is_dir={file_is_dir}"
