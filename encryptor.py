from cryptography.fernet import Fernet
from keygen import get_key
import utils
import os

class Encryptor:
    files_encrypted = 0

    @classmethod
    def encrypt_msg(cls, msg: str | bytes, password: str) -> bytes:
        encoded_text = msg.encode() if type(msg) == str else msg
        cipher = Fernet(get_key(password=password))
        encrypted_text = cipher.encrypt(encoded_text)

        return encrypted_text

    @classmethod
    def encrypt_file_content(cls, filepath: str, password: str, add_extension=False) -> bytes:
        try:
            with open(filepath, 'rb') as f:
                file_content = f.read()

                if add_extension:
                    file_content += utils.get_file_extension(filepath).encode()

                encrypted_content = cls.encrypt_msg(file_content, password)

                return encrypted_content
        except FileNotFoundError:
            print("File Not Found")

    @classmethod
    def encrypt_file(cls, filepath: str, password: str, save_directory: str, add_extension=True):
        try:
            encrypted_content = cls.encrypt_file_content(filepath, password, add_extension)

            save_file_name = utils.get_file_name(filepath, with_extension=True)
            encrypted_file_extension = ".enc"
            save_file_name += encrypted_file_extension
            save_file_path = save_directory + "\\" + save_file_name

            while os.path.exists(save_file_path):
                save_file_name = utils.add_nonduplicate_identifier(save_file_name)
                save_file_path = save_directory + "\\" + save_file_name

            with open(save_file_path, "wb") as f:
                f.write(encrypted_content)
        except FileNotFoundError:
            print("File Not Found")

    @classmethod
    def encrypt_files(cls, filepaths: list, password: str, save_directory: str, add_extension=True, on_file_encrypted=lambda x: None, on_encryption_complete=lambda x: None):
        try:
            total_files = len(filepaths)

            for filepath in filepaths:
                cls.encrypt_file(filepath, password, save_directory, add_extension)

                cls.files_encrypted += 1
                if on_file_encrypted != None:
                    on_file_encrypted(cls.files_encrypted)

            if on_encryption_complete != None:
                on_encryption_complete(total_files)
        except FileNotFoundError:
            print("File(s) Not Found")

    #Top level folders passed in cmd arguments; handle sub folders here separately
    @classmethod
    def encrypt_folder(cls, folderpath: str, password: str, savepath: str, on_file_encrypted=lambda x: None):
        try:
            foldername = utils.get_folder_name(folderpath)
            encrypted_folder_path = savepath + "\\" + f"{foldername}.enc"
            while os.path.exists(encrypted_folder_path):
                encrypted_folder_path += "(1)"
            os.mkdir(encrypted_folder_path)
            scan_dir = os.scandir(folderpath)
            for obj in scan_dir:
                if obj.is_dir():
                    cls.encrypt_folder(obj.path, password, encrypted_folder_path, on_file_encrypted)
                elif obj.is_file():
                    cls.encrypt_file(obj.path, password, encrypted_folder_path, True)
                    cls.files_encrypted += 1
                    if on_file_encrypted != None:
                        on_file_encrypted(cls.files_encrypted)
        except FileNotFoundError:
            print(f"Folder {encrypted_folder_path} could not be created.")

    #Top level folders passed in cmd arguments; handle sub folders separately
    @classmethod
    def encrypt_folders(cls, folderpaths: list, password: str, save_directory: str, on_file_encrypted=lambda x: None, on_encryption_complete=lambda x: None):
        try:
            total_folders = len(folderpaths)

            for folderpath in folderpaths:
                cls.encrypt_folder(folderpath, password, save_directory, on_file_encrypted)

            if on_encryption_complete != None:
                on_encryption_complete(total_folders)
        except FileNotFoundError:
            print("Folders(s) Not Found")
