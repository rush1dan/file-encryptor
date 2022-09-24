import tkinter as tk


def main_window():
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
    
    import data
    import pages

    initial_page = "Encrypt" if data.operation_mode == data.OperationMode.ENCRYPTION else "Decrypt"
    pages.setup_all_pages(main_window=window, window_width=windowWidth, window_height=windowHeight, start_page=initial_page)

    window.mainloop()