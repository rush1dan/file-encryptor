from enum import IntEnum

class OperationMode(IntEnum):
    ENCRYPTION = 0,
    DECRYPTION = 1

def set_data(operation_arg: str, files: list):
    global operation_mode
    global selected_files

    match operation_arg:
        case "--encrypt":
            operation_mode = OperationMode.ENCRYPTION
        case "--decrypt":
            operation_mode = OperationMode.DECRYPTION
        case _:
            print("Operation mode argument not passed properly.")

    selected_files = files