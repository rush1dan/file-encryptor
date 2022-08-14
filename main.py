import sys
import tkinter as tk

window = tk.Tk()

try:
    label = tk.Label(text=sys.argv[1])
except:
    label = tk.Label(text="No Args")

label.pack()

window.mainloop()
