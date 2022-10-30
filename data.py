from enum import IntEnum

class OperationObject(IntEnum):
    FILE = 0,
    FOLDER = 1

class OperationMode(IntEnum):
    ENCRYPTION = 0,
    DECRYPTION = 1

def set_data(operation_object_arg: str, operation_mode_arg: str, files_or_folders: list):
    global operation_object
    global operation_mode
    global selected_files_or_folders

    match operation_object_arg:
        case "--file":
            operation_object = OperationObject.FILE
        case "--folder":
            operation_object = OperationObject.FOLDER
        case _:
            print("Operation object argument not passed properly.")

    match operation_mode_arg:
        case "--encrypt":
            operation_mode = OperationMode.ENCRYPTION
        case "--decrypt":
            operation_mode = OperationMode.DECRYPTION
        case _:
            print("Operation mode argument not passed properly.")

    selected_files_or_folders = files_or_folders