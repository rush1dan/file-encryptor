import sys
import traceback
import data
import main_window
import os
import time

def run_from_right_click():
    main_window.main_window()


def run_as_standalone_application():
    print("Right Click Menu Not Configured Properly.")
    return None


if __name__ == "__main__":
    try:
        # Run Single Instance even for multiple files:
        if not os.path.exists("C:\\PythonProjects\\FileEnDecryptor\\Data\\Initialization.txt"):
            if not os.path.exists("C:\\PythonProjects\\FileEnDecryptor\\Data"):
                os.makedirs("C:\\PythonProjects\\FileEnDecryptor\\Data")
                open("C:\\PythonProjects\\FileEnDecryptor\\Data\\Initialization.txt", 'w').close()

        first_instance = False

        with open("C:\\PythonProjects\\FileEnDecryptor\\Data\\Initialization.txt", "r+", buffering=1) as file_init:
            lines = file_init.readlines()
            if len(lines) == 0:  # File not created yet, hence no instance running
                # Write the file path of the file selected
                file_init.seek(0, 2)
                file_init.write(sys.argv[2] + "\n")
                file_init.flush()

                first_instance = True

            else:  # File already created, hence one instance running
                file_init.seek(0, 2)
                file_init.write(sys.argv[2] + "\n")
                file_init.flush()

        if first_instance:
            #Wait for other files to conclude writing to the initializer:
            time.sleep(1.0)
            #Read all file paths from init file and store in list:
            with open("C:\\PythonProjects\\FileEnDecryptor\\Data\\Initialization.txt", "r") as file_init:
                selected_files = file_init.readlines()
            
            data.set_data(operation_arg=sys.argv[1], files=selected_files)

            #Erase the file for next session:
            with open("C:\\PythonProjects\\FileEnDecryptor\\Data\\Initialization.txt", "w") as file_init:
                file_init.write("")

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
