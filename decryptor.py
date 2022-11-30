from cryptography.fernet import Fernet, InvalidToken
from keygen import get_key
import utils
import os


class Decryptor:
    files_decrypted = 0

    @classmethod
    def decrypt_msg(cls, encrypted_msg: str | bytes, password: str) -> bytes:
        encoded_text = encrypted_msg.encode() if type(
            encrypted_msg) == str else encrypted_msg
        cipher = Fernet(get_key(password=password))
        
        decrypted_text = cipher.decrypt(encoded_text)

        return decrypted_text

    @classmethod
    def decrypt_file_content(cls, filepath: str, password: str, remove_extension = False) -> bytes:
        try:
            with open(filepath, 'rb') as f:
                file_content = f.read()
                decrypted_content = cls.decrypt_msg(file_content, password)

                if remove_extension:
                    decrypted_content = utils.remove_file_extension(decrypted_content)

                return decrypted_content
        except FileNotFoundError:
            print("File Not Found")

    @classmethod
    def decrypt_file(cls, filepath: str, password: str, save_directory: str):
        try:
            decrypted_content = cls.decrypt_file_content(filepath, password, remove_extension=False)    #Embedded file extension needs to be extracted
            
            save_file_name = utils.get_file_name(filepath, with_extension=False)

            og_file_extension = utils.get_original_file_extension(decrypted_content)
            decrypted_content = utils.remove_file_extension(decrypted_content)      #Embedded file extension can be removed after extracting it
            if not cls.name_has_og_extension(save_file_name, og_file_extension):      #If decrypted file already doesn't have the og extension, then add it
                save_file_name += og_file_extension  

            save_file_path = save_directory + "\\" + save_file_name

            while os.path.exists(save_file_path):
                save_file_name = utils.add_nonduplicate_identifier(save_file_name)
                save_file_path = save_directory + "\\" + save_file_name

            with open(save_file_path, "wb") as f:
                f.write(decrypted_content)
        except FileNotFoundError:
            print("File Not Found")

    @classmethod
    def decrypt_files(cls, filepaths: list, password: str, save_directory: str, 
        on_file_decrypted=lambda x: None, on_decryption_complete=lambda x: None, on_error=lambda x, y: None):
        try:
            total_files = len(filepaths)

            for filepath in filepaths:
                cls.decrypt_file(filepath, password, save_directory)

                cls.files_decrypted += 1
                if on_file_decrypted != None:
                    on_file_decrypted(cls.files_decrypted)

            if on_decryption_complete != None:
                on_decryption_complete(total_files)
        except InvalidToken:
            if on_error != None:
                on_error("Incorrect Password Error", "Incorrect password entered.\nDecryption failed.")
            return
        except FileNotFoundError:
            if on_error != None:
                on_error("File Not Found Error", "File Not Found.")
            return
        except Exception as ex:
            if on_error != None:
                on_error(type(ex).__name__, str(ex))
            return

    #Top level folders passed in cmd arguments; handle sub folders here separately
    @classmethod
    def decrypt_folder(cls, folderpath: str, password: str, savepath: str, on_file_decrypted=lambda x: None):
        try:
            foldername = utils.get_folder_name(folderpath)
            foldername = foldername.replace(".enc", "")
            decrypted_folder_path = savepath + "\\" + foldername
            while os.path.exists(decrypted_folder_path):
                decrypted_folder_path += "(1)"
            os.mkdir(decrypted_folder_path)
            scan_dir = os.scandir(folderpath)
            for obj in scan_dir:
                if obj.is_dir():
                    cls.decrypt_folder(obj.path, password, decrypted_folder_path, on_file_decrypted)
                elif obj.is_file():
                    cls.decrypt_file(obj.path, password, decrypted_folder_path)
                    cls.files_decrypted += 1
                    if on_file_decrypted != None:
                        on_file_decrypted(cls.files_decrypted)
        except FileNotFoundError:
            print(f"Folder {decrypted_folder_path} could not be created.")

    #Top level folders passed in cmd arguments; handle sub folders separately
    @classmethod
    def decrypt_folders(cls, folderpaths: list, password: str, save_directory: str, 
        on_file_decrypted=lambda x: None, on_decryption_complete=lambda x: None, on_error=lambda x, y: None):
        try:
            total_folders = len(folderpaths)

            for folderpath in folderpaths:
                cls.decrypt_folder(folderpath, password, save_directory, on_file_decrypted)

            if on_decryption_complete != None:
                on_decryption_complete(total_folders)
        except InvalidToken:
            if on_error != None:
                on_error("Incorrect Password Error", "Incorrect password entered.\nDecryption failed.")
            return
        except FileNotFoundError:
            if on_error != None:
                on_error("File Not Found Error", "File Not Found.")
            return
        except Exception as ex:
            if on_error != None:
                on_error(type(ex).__name__, str(ex))
            return

    @classmethod
    def name_has_og_extension(cls, filename_or_path: str, extension: str)->bool:
        return filename_or_path[len(filename_or_path) - len(extension) : ] == extension
