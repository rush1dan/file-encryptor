from doctest import master
import tkinter as tk


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.page_width = kwargs["width"]
        self.page_height = kwargs["height"]

        self.pack(side="top", fill="both", expand=True)

    def show(self):
        self.lift()


class Options_Page(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.rowconfigure(index=0, minsize=self.page_height/2)
        self.rowconfigure(index=1, minsize=self.page_height/2)
        self.columnconfigure(index=0, minsize=self.page_width)

        frm_label = tk.Frame(master=self, relief=tk.FLAT,
                             borderwidth=0, bg="red")
        frm_label.grid(row=0, column=0, sticky="nsew")
        lbl_options = tk.Label(
            master=frm_label, text="Encrypt or Decrypt?", font=("Arial", 15))
        lbl_options.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        frm_btn = tk.Frame(master=self, relief=tk.FLAT,
                           borderwidth=0, bg="green")
        frm_btn.grid(row=1, column=0, sticky="nsew")
        frm_btn.columnconfigure([0, 1], minsize=int(self.page_width/2))

        frm_btn_encrypt = tk.Frame(
            master=frm_btn, relief=tk.RAISED, borderwidth=0, bg="yellow")
        frm_btn_encrypt.grid(row=0, column=0, sticky="ns")
        btn_encrypt = tk.Button(master=frm_btn_encrypt,
                                text="Encrypt", command=None, font=("Arial", 15), border=6, borderwidth=6)
        btn_encrypt.pack(padx=10, pady=10)

        frm_btn_decrypt = tk.Frame(
            master=frm_btn, relief=tk.RAISED, borderwidth=0, bg="cyan")
        frm_btn_decrypt.grid(row=0, column=1, sticky="ns")
        btn_decrypt = tk.Button(master=frm_btn_decrypt,
                                text="Decrypt", command=None, font=("Arial", 15), border=6, borderwidth=6)
        btn_decrypt.pack(padx=10, pady=10)
