from enum import IntEnum
import os.path

class Data:
    SCREEN_RES_FACTOR = 1.0

    class OperationObject(IntEnum):
        FILE = 0,
        FOLDER = 1

    class OperationMode(IntEnum):
        ENCRYPTION = 0,
        DECRYPTION = 1

    operation_mode = None
    selected_files = []
    selected_folders = []

    @classmethod
    def set_data(cls, operation_mode_arg: str, files_or_folders: list)->bool:
        match operation_mode_arg:
            case "--encrypt":
                cls.operation_mode = cls.OperationMode.ENCRYPTION
            case "--decrypt":
                cls.operation_mode = cls.OperationMode.DECRYPTION
            case _:
                print("Operation mode argument not passed properly.")
                return False

        for path in files_or_folders:
            if os.path.isdir(path):
                cls.selected_folders.append(path)
            else:
                cls.selected_files.append(path)

        return True
