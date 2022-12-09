import tkinter as tk
from data import Data
from pages import Page_Manager

class Window_Manager:

    @classmethod
    def main_window(cls):
        window = tk.Tk()

        screenWidth = window.winfo_screenwidth()
        screenHeight = window.winfo_screenheight()
        screenAspectRatio = screenWidth / screenHeight

        windowAspectRatio = 1.5
        windowWidth = int(screenWidth / 6)
        windowHeight = int(windowWidth / windowAspectRatio)

        window.title("Simple File Encryptor")
        cls.center_window(window, windowWidth, windowHeight)
        photo = tk.PhotoImage(file = "C:\\PythonProjects\\FileEnDecryptor\\checkmark.png")
        window.wm_iconphoto(False, photo)

        initial_page = "Encrypt" if Data.operation_mode == Data.OperationMode.ENCRYPTION else "Decrypt"
        Page_Manager.setup_all_pages(main_window=window, window_width=windowWidth, window_height=windowHeight, start_page=initial_page)

        window.mainloop()

    @classmethod
    def center_window(cls, window, width=300, height=200):
            # get screen width and height
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()

            # calculate position x and y coordinates
            x = int((screen_width/2)) - int((width/2))
            y = int((screen_height/2)) - int((height/2))
            window.geometry(f'{width}x{height}+{x}+{y}')
            window.resizable(0, 0)