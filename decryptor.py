from cryptography.fernet import Fernet
from keygen import get_key
import utils


def decrypt_msg(encrypted_msg: str | bytes, password: str) -> bytes:
    encoded_text = encrypted_msg.encode() if type(
        encrypted_msg) == str else encrypted_msg
    cipher = Fernet(get_key(password=password))
    decrypted_text = cipher.decrypt(encoded_text)

    return decrypted_text


def decrypt_file_content(filepath: str, password: str, remove_extension = False) -> bytes:
    try:
        with open(filepath, 'rb') as f:
            file_content = f.read()
            decrypted_content = decrypt_msg(file_content, password)

            if remove_extension:
                decrypted_content = utils.remove_file_extension(decrypted_content)

            return decrypted_content
    except FileNotFoundError:
        print("File Not Found")

def decrypt_file(filepath: str, password: str, savepath: str):
    try:
        decrypted_content = decrypt_file_content(filepath, password, remove_extension=False)    #Embedded file extension needs to be extracted
        og_file_extension = utils.get_original_file_extension(decrypted_content)
        decrypted_content = utils.remove_file_extension(decrypted_content)      #Embedded file extension can be removed after extracting it
        if not name_has_og_extension(savepath, og_file_extension):      #If decrypted file already doesn't have the og extension, then add it
            savepath += og_file_extension   

        with open(savepath, "wb") as f:
            f.write(decrypted_content)
    except FileNotFoundError:
        print("File Not Found")

def decrypt_files(filepaths: list, password: str, save_directory: str, on_file_decrypted=lambda x: None, on_decryption_complete=lambda x: None):
    try:
        total_files = len(filepaths)
        files_processed = 0
        for filepath in filepaths:
            #file_directory = utils.get_file_directory(filepath)
            save_file_name = utils.get_file_name(filepath, with_extension=False)
            save_file_path_without_extension = save_directory + "\\" + save_file_name

            decrypt_file(filepath, password, save_file_path_without_extension)

            files_processed += 1
            if files_processed == total_files:
                if on_decryption_complete != None:
                    on_decryption_complete(total_files)
            else:
                if on_file_decrypted != None:
                    on_file_decrypted(files_processed)
    except FileNotFoundError:
        print("File(s) Not Found")

def name_has_og_extension(filename_or_path: str, extension: str)->bool:
    return filename_or_path[len(filename_or_path) - len(extension) : ] == extension
