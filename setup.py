from tkinter import messagebox
from tkinter import filedialog
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


def register_in_windows_registry(menu_name="", exefilepath=""):
    if is_admin():
        with winreg.ConnectRegistry(None, winreg.HKEY_CLASSES_ROOT) as hkey:
            with winreg.OpenKey(hkey, r'txtfile\shell') as subkey:
                winreg.CreateKey(subkey, menu_name)
                with winreg.OpenKey(subkey, menu_name) as menukey:
                    command_name = "command"
                    winreg.CreateKey(menukey, command_name)
                    with winreg.OpenKey(menukey, command_name, 0, winreg.KEY_WRITE) as commandkey:
                        winreg.SetValueEx(
                            commandkey, "", 0, winreg.REG_SZ, r"put\directory\here %1")
    else:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    return None


if __name__ == "__main__":
    app_dir = get_application_exe(os.path.dirname(os.path.realpath(__file__)))

    if app_dir != None:
        register_in_windows_registry(menu_name="File Encryptor", dir=app_dir)
    else:
        messagebox.showerror(title="Application Not Found Error",
                             message="FileEncryptor.exe not found. Did you move it somewhere else?")
