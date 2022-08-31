from enum import Enum, IntEnum
import sys
import main_window
import re


class OperationMode(IntEnum):
    ENCRYPTION = 0,
    DECRYPTION = 1


def run_from_right_click(arg):
    if re.search(r'\.enc$', arg):
        main_window.main_window(OperationMode.DECRYPTION)
    else:
        main_window.main_window(OperationMode.ENCRYPTION)


def run_as_standalone_application():
    print("Right Click Menu Not Configured Properly.")
    return None


if __name__ == "__main__":
    try:
        run_from_right_click(sys.argv[1])
    except:
        run_as_standalone_application()


# ***To Installer as .exe run command in the following way:***
# pyinstaller --onefile --paths C:\PythonProjects\FileEnDecryptor\.venv\Lib\site-packages main.py
# and rename the generated main.exe to SimpleFileEncryptor.exe

# Right click context menu based encryption decryption working
