from cryptography.fernet import Fernet
from keygen import get_key
import utils
import os


def encrypt_msg(msg: str | bytes, password: str) -> bytes:
    encoded_text = msg.encode() if type(msg) == str else msg
    cipher = Fernet(get_key(password=password))
    encrypted_text = cipher.encrypt(encoded_text)

    return encrypted_text

def encrypt_file_content(filepath: str, password: str, add_extension=False) -> bytes:
    try:
        with open(filepath, 'rb') as f:
            file_content = f.read()

            if add_extension:
                file_content += utils.get_file_extension(filepath).encode()

            encrypted_content = encrypt_msg(file_content, password)

            return encrypted_content
    except FileNotFoundError:
        print("File Not Found")

def encrypt_file(filepath: str, password: str, savepath: str, add_extension=True):
    try:
        encrypted_content = encrypt_file_content(filepath, password, add_extension)

        with open(savepath, "wb") as f:
            f.write(encrypted_content)
    except FileNotFoundError:
        print("File Not Found")

def encrypt_files(filepaths: list, password: str, save_directory: str, add_extension=True, on_file_encrypted=lambda x: None, on_encryption_complete=lambda x: None):
    try:
        total_files = len(filepaths)
        files_encrypted = 0

        for filepath in filepaths:
            #file_directory = utils.get_file_directory(filepath)
            save_file_name = utils.get_file_name(filepath, with_extension=True)
            encrypted_file_extension = ".enc"
            save_file_path = save_directory + "\\" + save_file_name + encrypted_file_extension

            encrypt_file(filepath, password, save_file_path, add_extension)

            files_encrypted += 1
            if on_file_encrypted != None:
                on_file_encrypted(files_encrypted)

        if on_encryption_complete != None:
            on_encryption_complete(total_files)
    except FileNotFoundError:
        print("File(s) Not Found")


#Top level folders passed in cmd arguments; handle sub folders here separately
def encrypt_folder(folderpath: str, password: str, savepath: str, on_file_encrypted=lambda x: None):
    try:
        for dir, sub_dirname_list, filename_list in os.walk(folderpath):
            #Create a folder structure similar to what was found in the original folder hierarchy
            try:
                encrypted_folder_path = savepath + "\\" + utils.get_folder_name(dir) + ".enc"
                os.mkdir(encrypted_folder_path)
            except Exception:
                print(f"Directory {encrypted_folder_path} could not be created.")
                return

            filepaths = [dir + "\\" + filename for filename in filename_list]
            encrypt_files(filepaths, password, encrypted_folder_path, True, on_file_encrypted=on_file_encrypted, on_encryption_complete=None)
    except FileNotFoundError:
        print("Folder Not Found")

#Top level folders passed in cmd arguments; handle sub folders separately
def encrypt_folders(folderpaths: list, password: str, save_directory: str, on_file_encrypted=lambda x: None, on_encryption_complete=lambda x: None):
    try:
        total_folders = len(folderpaths)

        for folderpath in folderpaths:
            encrypt_folder(folderpath, password, save_directory, on_file_encrypted)

        if on_encryption_complete != None:
            on_encryption_complete(total_folders)
    except FileNotFoundError:
        print("Folders(s) Not Found")
