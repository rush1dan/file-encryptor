import time
import tkinter as tk

def center_window(window: tk.Tk, width=300, height=200):
    # get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # calculate position x and y coordinates
    x = int((screen_width/2)) - int((width/2))
    y = int((screen_height/2)) - int((height/2))
    window.geometry(f'{width}x{height}+{x}+{y}')

def show_progress():
    progress_window = tk.Tk()
    progress_window.title("Progress")

    screenWidth = progress_window.winfo_screenwidth()
    screenHeight = progress_window.winfo_screenheight()
    screenAspectRatio = screenWidth / screenHeight

    windowAspectRatio = 6
    windowWidth = int(screenWidth / 5)
    windowHeight = int(windowWidth / windowAspectRatio)

    progress_window.resizable(0, 0)

    center_window(progress_window, width=windowWidth, height=windowHeight)
    
    files_encrypted = 1
    dots = ""
    text = "Encrypting Files {files_encrypted}/3".format(files_encrypted=files_encrypted)

    label = tk.Label(master=progress_window, text=text, font=("Arial", 15))
    label.pack()

    while True:
        time.sleep(1)
        dots += "."
        if len(dots) > 3:
            dots = ""
        label.config(text=text + dots)
        progress_window.update()
    #progress_window.mainloop()


show_progress()


