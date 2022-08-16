import tkinter as tk

window = tk.Tk()

screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()
screenAspectRatio = screenWidth / screenHeight

windowWidth = int(screenWidth / 6)
windowHeight = int(windowWidth / screenAspectRatio)

window.title("File Encryption")
window.geometry(f"{windowWidth}x{windowHeight}")
window.resizable(0, 0)
window.rowconfigure(index=0, minsize=windowHeight/2)
window.rowconfigure(index=1, minsize=windowHeight/2)
window.columnconfigure(index=0, minsize=windowWidth)

frm_label = tk.Frame(master=window, relief=tk.FLAT, borderwidth=0)
frm_label.grid(row=0, column=0)
lbl_options = tk.Label(
    master=frm_label, text="Encrypt or Decrypt?", font=("Arial", 15))
lbl_options.pack()

frm_btn = tk.Frame(master=window, relief=tk.FLAT, borderwidth=0)
frm_btn.grid(row=1, column=0)
frm_btn.columnconfigure([0, 1], minsize=int(windowWidth/2))

frm_btn_encrypt = tk.Frame(master=frm_btn, relief=tk.RAISED, borderwidth=0)
frm_btn_encrypt.grid(row=0, column=0)
btn_encrypt = tk.Button(master=frm_btn_encrypt,
                        text="Encrypt", command=None, font=("Arial", 15), border=6, borderwidth=6)
btn_encrypt.pack(padx=10, pady=10)

frm_btn_decrypt = tk.Frame(master=frm_btn, relief=tk.RAISED, borderwidth=0)
frm_btn_decrypt.grid(row=0, column=1)
btn_decrypt = tk.Button(master=frm_btn_decrypt,
                        text="Decrypt", command=None, font=("Arial", 15), border=6, borderwidth=6)
btn_decrypt.pack(padx=10, pady=10)

window.mainloop()
