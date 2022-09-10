from tkinter import messagebox
import os
import winreg
import ctypes
import sys


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def get_application_exe(dir):
    for dir_name, sub_dir_list, file_list in os.walk(dir):
        for file_name in file_list:
            if file_name == "SimpleFileEncryptor.exe":
                return dir_name + "\\" + file_name

    return None


def register_in_windows_registry(encryption_menu_name="", decryption_menu_name="", exefilepath=""):
    if is_admin():
        with winreg.ConnectRegistry(None, winreg.HKEY_CLASSES_ROOT) as hkey:

            # Set Encryptor:
            # Configure It With Right Click Context Menu
            with winreg.OpenKey(hkey, r'*\shell') as subkey:
                winreg.CreateKey(subkey, encryption_menu_name)
                with winreg.OpenKey(subkey, encryption_menu_name, 0, winreg.KEY_WRITE) as encryption_menukey:
                    winreg.SetValueEx(encryption_menukey, "", 0, winreg.REG_SZ, "Encrypt File(s)")
                    winreg.SetValueEx(encryption_menukey, "AppliesTo",
                                      0, winreg.REG_SZ, "NOT System.FileExtension:=.enc")
                    command_name = "command"
                    winreg.CreateKey(encryption_menukey, command_name)
                    with winreg.OpenKey(encryption_menukey, command_name, 0, winreg.KEY_WRITE) as commandkey:
                        winreg.SetValueEx(commandkey, "", 0, winreg.REG_SZ, f"\"{exefilepath}\" --encrypt %1")

            # Set Decryptor:
            encrypted_file_extension = ".enc"
            encrypted_file_type = "encfile"

            # Create New Encrypted File Type in Registry and Configure It With Right Click Context Menu
            winreg.CreateKey(hkey, encrypted_file_type)
            with winreg.OpenKey(hkey, encrypted_file_type) as encrypted_file_type_key:
                winreg.CreateKey(encrypted_file_type_key, "shell")
                with winreg.OpenKey(encrypted_file_type_key, "shell") as shellkey:
                    winreg.CreateKey(shellkey, decryption_menu_name)
                    with winreg.OpenKey(shellkey, decryption_menu_name) as decryption_menukey:
                        winreg.SetValueEx(decryption_menukey, "", 0, winreg.REG_SZ, "Decrypt File(s)")
                        command_name = "command"
                        winreg.CreateKey(decryption_menukey, command_name)
                        with winreg.OpenKey(decryption_menukey, command_name, 0, winreg.KEY_WRITE) as commandkey:
                            winreg.SetValueEx(commandkey, "", 0, winreg.REG_SZ, f"\"{exefilepath}\" --decrypt %1")

            # Create New Encrypted File Extension in Registry and register newly created Encrypted File Type under it
            # and configure the extension to behave similar to a .txt extension
            winreg.CreateKey(hkey, encrypted_file_extension)
            with winreg.OpenKey(hkey, encrypted_file_extension, 0, winreg.KEY_WRITE) as encrypted_file_extension_key:
                winreg.SetValueEx(encrypted_file_extension_key, "", 0, winreg.REG_SZ, encrypted_file_type)
                winreg.SetValueEx(encrypted_file_extension_key, "Content Type", 0, winreg.REG_SZ, "text/plain")
                winreg.SetValueEx(encrypted_file_extension_key, "PerceivedType", 0, winreg.REG_SZ, "text")

    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    return None


if __name__ == "__main__":
    app_dir = get_application_exe(os.path.dirname(os.path.realpath(__file__)))

    if app_dir != None:
        register_in_windows_registry(encryption_menu_name="Encrypt", decryption_menu_name="Decrypt", exefilepath=app_dir)
    else:
        messagebox.showerror(title="Application Not Found Error",
                             message="FileEncryptor.exe not found. Did you move it somewhere else?")
