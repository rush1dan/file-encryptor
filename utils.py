import os

def get_file_name(filepath: str, with_extension: bool = True):
    filename_rev = ""
    for i in range(len(filepath) - 1, -1, -1):
        ch = filepath[i]
        if ch == "/" or ch == "\\":
            break
        filename_rev += ch

        filename = filename_rev[::-1]
    return filename if with_extension else filename.replace(get_file_extension(filename), "")


def get_file_extension(filename: str):
    extension_rev = ""
    for i in range(len(filename) - 1, -1, -1):
        ch = filename[i]
        extension_rev += ch
        if ch == ".":
            break
    return extension_rev[::-1]


def get_original_file_extension(decrypted_content: bytes) -> str:

    """ Extracts the embedded file extension """

    extension_rev = b""
    for i in range(len(decrypted_content) - 1, -1, -1):
        ch_int = decrypted_content[i]
        ch_byte = int_to_bytes(ch_int)
        extension_rev += ch_byte
        if ch_byte == b".":
            break
    return extension_rev[::-1].decode()


def remove_file_extension(decrypted_content: bytes) -> bytes:

    """ Removes the embedded file extension """

    for i in range(len(decrypted_content) - 1, -1, -1):
        ch_int = decrypted_content[i]
        ch_byte = int_to_bytes(ch_int)
        if ch_byte == b".":
            return decrypted_content[:i]

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def get_file_directory(filepath: str) -> str:
    return os.path.dirname(os.path.realpath(filepath))
