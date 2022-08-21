import tkinter as tk
import pages

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

# options_page = pages.Options_Page(
#     master=window, width=windowWidth, height=windowHeight)
# options_page.show()

# encryption_page = pages.Encryption_Page(
#     master=window, width=windowWidth, height=windowHeight)
# encryption_page.show()

decryption_page = pages.Decryption_Page(
    master=window, width=windowWidth, height=windowHeight)
decryption_page.show()

window.mainloop()
