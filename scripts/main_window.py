import tkinter as tk
from data import Data
from page_manager import Page_Manager
from tkinter import messagebox
import base64

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
        #from https://www.motobit.com/util/base64-decoder-encoder.asp, 32*32 png to utf-8 base64 string
        base64_png = "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"
        img_data_bytes = base64.b64decode(base64_png)
        photo_icon = tk.PhotoImage(data= img_data_bytes)
        window.wm_iconphoto(True, photo_icon)

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

    @classmethod
    def show_info_window_only(cls, title: str, msg: str):
        messagebox.showinfo(title=title, message=msg)