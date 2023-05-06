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


def get_file_extension(filename_or_path: str):
    extension_rev = ""
    for i in range(len(filename_or_path) - 1, -1, -1):
        ch = filename_or_path[i]
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

def get_parent_directory(file_or_folder_path: str) -> str:
    return os.path.dirname(os.path.realpath(file_or_folder_path))

def get_folder_name(folderpath: str):
    foldername_rev = ""
    for i in range(len(folderpath) - 1, -1, -1):
        ch = folderpath[i]
        if ch == "/" or ch == "\\":
            break
        foldername_rev += ch

        foldername = foldername_rev[::-1]
    return foldername

def get_all_files_under_directory(directory: str)->list:
    all_files_list = []
    for dir, sub_dirname_list, filename_list in os.walk(directory):
        all_files_list.extend([dir + "\\" + filename for filename in filename_list])
    return all_files_list

def get_all_files_under_directory_with_extension(directory: str, file_extension: str)->list:
    all_files_list = []
    for dir, sub_dirname_list, filename_list in os.walk(directory):
        all_files_list.extend([dir + "\\" + filename for filename in filename_list if get_file_extension(filename) == file_extension])
    return all_files_list

def get_all_filenames_under_directory(directory: str)->list:
    all_files_list = []
    for dir, sub_dirname_list, filename_list in os.walk(directory):
        all_files_list.extend(filename_list)
    return all_files_list

def get_all_filescount_under_directory(directory: str)->int:
    file_count = 0
    for dir, sub_dirname_list, filename_list in os.walk(directory):
        file_count += len(filename_list)
    return file_count

def add_nonduplicate_identifier(filename_or_path: str)->str:
    file_extension = get_file_extension(filename_or_path)
    modified_filename_or_path = filename_or_path.replace(file_extension, f"(1){file_extension}")
    return modified_filename_or_path
