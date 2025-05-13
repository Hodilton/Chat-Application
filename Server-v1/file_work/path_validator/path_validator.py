import os

from ..utils.utilities import Messages, Check

class PathValidator:
    @staticmethod
    def for_read(folder_path, file_name, extension, valid_extensions):
        if not PathValidator.validate_path(folder_path, "directory"):
            Messages.Error.folder_not_found(fr"{PathValidator.get_project_relative_path()}\{folder_path}")
            return False

        path = PathValidator.get_full_path(folder_path, file_name, extension)

        if not PathValidator.validate_path(path, "extension", valid_extensions, extension):
            Messages.Error.file_extension(fr"{PathValidator.get_project_relative_path()}\{path}", valid_extensions)
            return False

        if not PathValidator.validate_path(path, "file"):
            Messages.Error.file_not_found(fr"{PathValidator.get_project_relative_path()}\{path}")
            return False

        return True

    @staticmethod
    def for_write(folder_path, file_name, extension, valid_extensions, overwrite):
        if not PathValidator.validate_path(folder_path, "directory"):
            Messages.Error.folder_not_found(fr"{PathValidator.get_project_relative_path()}\{folder_path}")
            return False

        path = PathValidator.get_full_path(folder_path, file_name, extension)

        if not PathValidator.validate_path(path, "extension", valid_extensions, extension):
            Messages.Error.file_extension(fr"{PathValidator.get_project_relative_path()}\{path}", valid_extensions)
            return False

        if PathValidator.validate_path(path, "file") and not overwrite:
            Messages.Error.file_found(fr"{PathValidator.get_project_relative_path()}\{path}")
            return False

        return True

    @staticmethod
    def extract_path(path_params):
        specified_keys = ["folder_path", "file_name", "extension"]

        if not Check.dictionary_specified(path_params, specified_keys):
            Messages.Error.specified_dictionary(specified_keys)
            return None

        folder_path = path_params.get("folder_path", "")
        file_name = path_params.get("file_name", "")
        extension = path_params.get("extension", "")
        return folder_path, file_name, extension

    @staticmethod
    def validate_path(file_path, check_type=None, valid_extensions=None, extension=None):
        if check_type == 'file' and not Check.file_file(file_path):
            return False
        if check_type == 'directory' and not Check.file_directory(file_path):
            return False
        if check_type == 'extension' and not Check.file_extension(extension, valid_extensions):
            return False
        return True

    @staticmethod
    def get_full_path(folder_path, file_name, expansion):
        return os.path.join(folder_path, file_name + '.' + expansion)

    @staticmethod
    def get_project_relative_path():
        current_dir = os.getcwd()
        project_dir = os.path.abspath(__file__)

        while not os.path.isfile(os.path.join(project_dir, '__init__.py')):
            project_dir = os.path.dirname(project_dir)

        relative_path = os.path.relpath(current_dir, start=project_dir)
        return relative_path
