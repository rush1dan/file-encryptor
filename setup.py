from fileinput import filename
from tkinter import messagebox
import os
import winreg


def get_application_exe(dir):
    for dir_name, sub_dir_list, file_list in os.walk(dir):
        for file_name in file_list:
            if file_name == "FileEncryptor.exe":
                return dir_name + "\\" + file_name

    return None


def register_in_windows_registry(exefilepath):
    return None


if __name__ == "__main__":
    app = get_application_exe(os.path.dirname(os.path.realpath(__file__)))

    if app != None:
        register_in_windows_registry(app)
    else:
        messagebox.showerror(title="Application Not Found Error",
                             message="FileEncryptor.exe not found. Did you move it somewhere else?")
