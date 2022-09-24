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

def animate_label(window: tk.Tk, label: tk.Label, files_encrypting: int, text: str, dots: str):
    #text.format(files_encrypto)
    dots += "."
    if len(dots) > 3:
        dots = ""
    label.config(text=text + dots)
    window.after(1000, lambda: animate_label(window, label, 1, text, dots))

def increase_file():
    global files_encrypto
    files_encrypto = 1

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

    dots = ""
    text = "Encrypting Files {}/3".format(1)

    label = tk.Label(master=progress_window, text=text, font=("Arial", 15))
    label.pack()

    button = tk.Button(master=progress_window, text="Click", command=increase_file)
    button.pack()

    animate_label(window=progress_window, label=label, files_encrypting=-1, text=text, dots=dots)

    progress_window.mainloop()

show_progress()


