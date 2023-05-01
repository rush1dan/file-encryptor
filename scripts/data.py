from enum import IntEnum

class Data:
    class OperationObject(IntEnum):
        FILE = 0,
        FOLDER = 1

    class OperationMode(IntEnum):
        ENCRYPTION = 0,
        DECRYPTION = 1

    operation_object = None
    operation_mode = None
    selected_files_or_folders = None

    @classmethod
    def set_data(cls, operation_object_arg: str, operation_mode_arg: str, files_or_folders: list):
        match operation_object_arg:
            case "--file":
                cls.operation_object = cls.OperationObject.FILE
            case "--folder":
                cls.operation_object = cls.OperationObject.FOLDER
            case _:
                print("Operation object argument not passed properly.")

        match operation_mode_arg:
            case "--encrypt":
                cls.operation_mode = cls.OperationMode.ENCRYPTION
            case "--decrypt":
                cls.operation_mode = cls.OperationMode.DECRYPTION
            case _:
                print("Operation mode argument not passed properly.")

        cls.selected_files_or_folders = files_or_folders