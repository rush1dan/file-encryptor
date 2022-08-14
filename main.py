import sys
import tkinter as tk
import os

window = tk.Tk()

try:
    label = tk.Label(text=sys.argv[1])
except:
    label = tk.Label(text="No Args")

label.pack()

print(f'File path is : {os.path.abspath(__file__)}')

window.mainloop()
