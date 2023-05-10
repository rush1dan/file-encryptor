from cryptography.fernet import Fernet
from keygen import get_key
import utils
import os
from traceback import print_exc as print_error

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
        with open(filepath, 'rb') as f:
            file_content = f.read()

            if add_extension:
                file_content += utils.get_file_extension(filepath).encode()

            encrypted_content = cls.encrypt_msg(file_content, password)

            return encrypted_content

    @classmethod
    def encrypt_file(cls, filepath: str, password: str, save_directory: str, add_extension=True,
                     on_file_encrypting=lambda index, file: None, on_file_encrypted=lambda decrypted_count: None, 
                     on_error=lambda title, msg: None):
        if on_file_encrypting != None:
            on_file_encrypting(cls.files_encrypted, filepath)
        
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
            if on_error != None:
                on_error("FileNotFoundError", f"No such file or directory: {filepath}")
            return
        
        cls.files_encrypted += 1
        if on_file_encrypted != None:
            on_file_encrypted(cls.files_encrypted)

    #Entry point method for encryption of files
    @classmethod
    def encrypt_files(cls, filepaths: list, password: str, save_directory: str, add_extension=True, 
        on_file_encrypting=lambda index, file: None, on_file_encrypted=lambda encrypted_count: None, on_encryption_complete=lambda x: None, 
        on_error=lambda title, msg: None):
        try:
            total_files = len(filepaths)

            for filepath in filepaths:
                cls.encrypt_file(filepath, password, save_directory, add_extension, 
                                 on_file_encrypting, on_file_encrypted, on_error)

            if on_encryption_complete != None:
                on_encryption_complete(total_files)
        except Exception as ex:
            print_error()
            if on_error != None:
                on_error(type(ex).__name__, str(ex))
            return

    #Top level folders passed in cmd arguments; handle sub folders here separately
    @classmethod
    def encrypt_folder(cls, folderpath: str, password: str, savepath: str, 
                       on_file_encrypting=lambda index, file: None, on_file_encrypted=lambda encrypted_count: None,
                       on_error=lambda title, msg: None):
        try:
            foldername = utils.get_folder_name(folderpath)
            encrypted_folder_path = savepath + "\\" + f"{foldername}.enc"
            while os.path.exists(encrypted_folder_path):
                encrypted_folder_path += "(1)"
            os.mkdir(encrypted_folder_path)
            scan_dir = os.scandir(folderpath)
            for obj in scan_dir:
                if obj.is_dir():
                    cls.encrypt_folder(obj.path, password, encrypted_folder_path,
                                    on_file_encrypting, on_file_encrypted, on_error)
                elif obj.is_file():
                    cls.encrypt_file(obj.path, password, encrypted_folder_path, True,
                                    on_file_encrypting, on_file_encrypted, on_error)
        except FileNotFoundError:
            if on_error != None:
                on_error("FileNotFoundError", f"No such file or directory: {folderpath}")

    #Top level folders passed in cmd arguments; handle sub folders separately
    @classmethod
    def encrypt_folders(cls, folderpaths: list, password: str, save_directory: str, 
        on_file_encrypting=lambda index, file: None, on_file_encrypted=lambda encrypted_count: None, on_encryption_complete=lambda encrypted_count: None, 
        on_error=lambda title, msg: None):
        try:
            total_folders = len(folderpaths)

            for folderpath in folderpaths:
                cls.encrypt_folder(folderpath, password, save_directory,
                                   on_file_encrypting, on_file_encrypted, on_error)

            if on_encryption_complete != None:
                on_encryption_complete(total_folders)
        except Exception as ex:
            print_error()
            if on_error != None:
                on_error(type(ex).__name__, str(ex))
            return
