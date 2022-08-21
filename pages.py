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

        self.rowconfigure(index=0, minsize=int(self.page_height/2))
        self.rowconfigure(index=1, minsize=int(self.page_height/2))
        self.columnconfigure(index=0, minsize=int(self.page_width))

        frm_label = tk.Frame(master=self, relief=tk.FLAT,
                             borderwidth=0)
        frm_label.grid(row=0, column=0, sticky="nsew")
        lbl_options = tk.Label(
            master=frm_label, text="Encrypt or Decrypt?", font=("Arial", 15))
        lbl_options.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        frm_btn = tk.Frame(master=self, relief=tk.FLAT,
                           borderwidth=0)
        frm_btn.grid(row=1, column=0, sticky="nsew")
        # frm_btn.rowconfigure(0, minsize=int(self.page_height/2))
        frm_btn.columnconfigure([0, 1], minsize=int(self.page_width/2))

        frm_btn_encrypt = tk.Frame(
            master=frm_btn, relief=tk.RAISED, borderwidth=0)
        frm_btn_encrypt.grid(row=0, column=0)
        btn_encrypt = tk.Button(master=frm_btn_encrypt,
                                text="Encrypt", command=None, font=("Arial", 15), border=6, borderwidth=6)
        btn_encrypt.pack(pady=20)

        frm_btn_decrypt = tk.Frame(
            master=frm_btn, relief=tk.RAISED, borderwidth=0)
        frm_btn_decrypt.grid(row=0, column=1)
        btn_decrypt = tk.Button(master=frm_btn_decrypt,
                                text="Decrypt", command=None, font=("Arial", 15), border=6, borderwidth=6)
        btn_decrypt.pack(pady=20)


class Encryption_Page(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        frm_backbutton = tk.Frame(master=self, relief=tk.RAISED, borderwidth=0)
        frm_backbutton.place(relx=0, rely=0, anchor="nw")

        btn_back = tk.Button(master=frm_backbutton, text="<=",
                             command=None, font=("Arial", 10), border=6, borderwidth=6)
        btn_back.pack()

        rows = 4
        self.rowconfigure([0, 1, 2, 3], minsize=self.page_height/4)
        self.columnconfigure(0, minsize=self.page_width)

        frm_enterpassword = tk.Frame(
            master=self, relief=tk.FLAT, borderwidth=0)
        # frm_enterpassword.grid(row=1, column=0, sticky="nsew")
        frm_enterpassword.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        ent_enterpassword = tk.Entry(master=frm_enterpassword)
        ent_enterpassword.pack()

        frm_confirmpassword = tk.Frame(
            master=self, relief=tk.FLAT, borderwidth=0, bg="green")
        frm_confirmpassword.grid(row=2, column=0, sticky="nsew")

        frm_btn_encrypt = tk.Frame(
            master=self, relief=tk.FLAT, borderwidth=0, bg="blue")
        frm_btn_encrypt.grid(row=3, column=0, sticky="nsew")

    def infocus(self, entry_widget: tk.Entry):
        entry_widget.config(show="")

    def outfocus(self, entry_widget: tk.Entry):
        entry_widget.config(show="")
