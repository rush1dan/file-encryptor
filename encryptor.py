from cryptography.fernet import Fernet
from keygen import get_key
import utils

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

def encrypt_files(filepaths: list, password: str, add_extension=True, on_file_encrypted = lambda x : None):
    try:
        files_processed = 0
        for filepath in filepaths:
            file_directory = utils.get_file_directory(filepath)
            save_file_name = utils.get_file_name(filepath, with_extension=True)
            encrypted_file_extension = ".enc"
            save_file_path = file_directory + "\\" + save_file_name + encrypted_file_extension

            encrypt_file(filepath, password, save_file_path, add_extension)

            files_processed += 1
            if on_file_encrypted != None:
                on_file_encrypted(files_processed)
    except FileNotFoundError:
        print("File(s) Not Found")
