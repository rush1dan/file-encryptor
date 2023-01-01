import sys
import traceback
from data import Data
from main_window import Window_Manager


def run_from_right_click():
    Window_Manager.main_window()

def run_as_standalone_application():
    print("Right Click Menu Not Configured Properly.")
    return None

def process_cmd_args()->tuple[str, str, list]:
    """Returns the Operation Object, Operation Mode and Selected Files or Folders"""
    return sys.argv[0], sys.argv[1], sys.argv[2:]

if __name__ == "__main__":
    try:
        operation_object, operation_mode, selected_files_or_folders = process_cmd_args()

        #Set operation and file data:
        Data.set_data(operation_object_arg=operation_object, operation_mode_arg=operation_mode, files_or_folders=selected_files_or_folders)

        # Run the program:
        try:
            run_from_right_click()
        except:
            run_as_standalone_application()
                
    except Exception as ex:
        traceback.print_exc()
        input("Press Enter To Exit...")


# ***To Install as .exe run command in the following way:***
# pyinstaller --onefile --paths C:\PythonProjects\FileEnDecryptor\.venv\Lib\site-packages main.py
# and to have it without the console run command:
# pyinstaller --onefile -w --paths C:\PythonProjects\FileEnDecryptor\.venv\Lib\site-packages main.py

# Right click context menu based encryption decryption working
