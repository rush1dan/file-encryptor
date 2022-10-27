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
    center_window(window, windowWidth, windowHeight)
    
    import data
    import pages

    initial_page = "Encrypt" if data.operation_mode == data.OperationMode.ENCRYPTION else "Decrypt"
    pages.setup_all_pages(main_window=window, window_width=windowWidth, window_height=windowHeight, start_page=initial_page)

    window.mainloop()

def center_window(window, width=300, height=200):
        # get screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # calculate position x and y coordinates
        x = int((screen_width/2)) - int((width/2))
        y = int((screen_height/2)) - int((height/2))
        window.geometry(f'{width}x{height}+{x}+{y}')
        window.resizable(0, 0)