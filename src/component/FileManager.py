from typing import BinaryIO

from component.ConfigManager import config_manager

upload_path = config_manager.get_value('media', 'upload')

class FileManager:
    """
    Manager file repo of server
    """
    def save_binary(self, file: BinaryIO, file_name: str) -> str:
        """
        :param file:
        :param file_name:
        :return:
        """
        file_path = f"{upload_path}/{file_name}"
        with open(f"{upload_path}/{file_name}", 'wb') as f:
            f.write(file.read())
        return file_path

    def get_binary_io(self, local_file_url: str) -> BinaryIO:
        """
        :param file_name:
        :return:
        """
        file_path = local_file_url.lstrip('file:/')
        try:
            with open(file_path, 'rb') as f:
                return f
        except Exception as e:
            raise IOError(f"cannot read file, file_path={file_path}, err: {e}")


file_manager : FileManager = FileManager()