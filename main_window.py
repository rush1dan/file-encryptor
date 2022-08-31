import tkinter as tk
from main import OperationMode
import pages


def main_window(operation_mode: OperationMode):
    window = tk.Tk()

    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    screenAspectRatio = screenWidth / screenHeight

    windowAspectRatio = 1.5
    windowWidth = int(screenWidth / 6)
    windowHeight = int(windowWidth / windowAspectRatio)

    window.title("Simple File Encryptor")
    window.geometry(f"{windowWidth}x{windowHeight}")
    window.resizable(0, 0)

    initial_page = "Encrypt" if operation_mode == OperationMode.ENCRYPTION else "Decrypt"
    pages.setup_all_pages(main_window=window,
                          window_width=windowWidth, window_height=windowHeight, start_page=initial_page)

    window.mainloop()
