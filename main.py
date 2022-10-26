import sys
import traceback
import data
import main_window


def run_from_right_click():
    main_window.main_window()

def run_as_standalone_application():
    print("Right Click Menu Not Configured Properly.")
    return None

def process_cmd_args()->tuple[str, list]:
    """Returns the Operation Mode and Selected Files"""
    return sys.argv[0], sys.argv[1:]

if __name__ == "__main__":
    try:
        operation_mode, selected_files = process_cmd_args()

        #Set operation and file data:
        data.set_data(operation_arg=operation_mode, files=selected_files)

        # Run the program:
        try:
            run_from_right_click()
        except:
            run_as_standalone_application()
                
    except Exception as ex:
        traceback.print_exc()
        input("Press Enter To Exit...")


# ***To Installer as .exe run command in the following way:***
# pyinstaller --onefile --paths C:\PythonProjects\FileEnDecryptor\.venv\Lib\site-packages main.py
# and rename the generated main.exe to SimpleFileEncryptor.exe

# Right click context menu based encryption decryption working
