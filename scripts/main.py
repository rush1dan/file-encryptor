import sys
from traceback import print_exc as print_error
from data import Data
from main_window import Window_Manager


def run_from_right_click():
    Window_Manager.main_window()

def run_as_standalone_application():
    Window_Manager.show_info_window_only(title="File Encryptor", msg="Use application from right click context menu.")
    return None

def process_cmd_args()->tuple[str, list]:
    """Returns the Operation Mode and Selected Files or Folders"""
    return sys.argv[0], sys.argv[1:]

if __name__ == "__main__":
    try:
        operation_mode, selected_files_or_folders = process_cmd_args()

        #Set operation and file data:
        if Data.set_data(operation_mode_arg=operation_mode, files_or_folders=selected_files_or_folders):
            run_from_right_click()
        else:
            run_as_standalone_application()
    except Exception as ex:
        Window_Manager.show_error_window_only(type(ex).__name__, str(ex))
        print_error()
        input("Press Enter To Exit...")


# ***To Install as .exe run command in the following way:***
# pyinstaller --onefile --paths C:\PythonProjects\FileEnDecryptor\.venv\Lib\site-packages main.py
# and to have it without the console run command:
# pyinstaller --onefile -w --paths C:\PythonProjects\FileEnDecryptor\.venv\Lib\site-packages main.py
# to avoid slower start time of single exectuable file with --onefile, compile with --onedir instead

# Right click context menu based encryption decryption working
