from ..factories.file_handler_factory import FileHandlerFactory
from ..path_validator.path_validator import PathValidator
from ..utils.utilities import Messages

class FileProcessor:
    @staticmethod
    def read_file(path_params):
        folder_path, file_name, extension = PathValidator.extract_path(path_params)

        data = None
        path = PathValidator.get_full_path(folder_path, file_name, extension)

        if PathValidator.for_read(folder_path, file_name, extension, ['json', 'csv', 'bin']):
            file_handler = FileHandlerFactory.create_handler(extension)
            data = file_handler.read(path)

        if data is not None:
            Messages.Complete.data_read(fr"{PathValidator.get_project_relative_path()}\{path}")
        else:
            Messages.Error.data_read(fr"{PathValidator.get_project_relative_path()}\{path}")
        return data

    @staticmethod
    def write_file(path_params, data, overwrite=False):
        folder_path, file_name, extension = PathValidator.extract_path(path_params)

        is_success = False
        path = PathValidator.get_full_path(folder_path, file_name, extension)

        if PathValidator.for_write(folder_path, file_name, extension, ['json', 'csv', 'bin'], overwrite):
            file_handler = FileHandlerFactory.create_handler(extension)
            is_success = file_handler.write(path, data, overwrite)

        if is_success:
            Messages.Complete.data_write(fr"{PathValidator.get_project_relative_path()}\{path}")
        else:
            Messages.Error.data_write(fr"{PathValidator.get_project_relative_path()}\{path}")

        return is_success
