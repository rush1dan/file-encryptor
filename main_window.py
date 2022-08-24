import tkinter as tk
import pages


def main_window():
    window = tk.Tk()

    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    screenAspectRatio = screenWidth / screenHeight

    windowAspectRatio = 1.5
    windowWidth = int(screenWidth / 6)
    windowHeight = int(windowWidth / windowAspectRatio)

    window.title("File Encryption")
    window.geometry(f"{windowWidth}x{windowHeight}")
    window.resizable(0, 0)

    pages.setup_all_pages(main_window=window,
                          window_width=windowWidth, window_height=windowHeight, start_page="Options")

    window.mainloop()
