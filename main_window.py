import tkinter as tk
import pages

window = tk.Tk()

screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()
screenAspectRatio = screenWidth / screenHeight

windowWidth = int(screenWidth / 6)
windowHeight = int(windowWidth / screenAspectRatio)

window.title("File Encryption")
window.geometry(f"{windowWidth}x{windowHeight}")
window.resizable(0, 0)

options_page = pages.Options_Page(
    master=window, width=windowWidth, height=windowHeight)
options_page.show()

window.mainloop()
