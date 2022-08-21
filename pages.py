import tkinter as tk

page_collection = {}


def setup_all_pages(main_window: tk.Widget, window_width: int, window_height: int, start_page: str):

    options_page = Options_Page(
        master=main_window, width=window_width, height=window_height)
    page_collection["Options"] = options_page

    encryption_page = Encryption_Page(
        master=main_window, width=window_width, height=window_height)
    page_collection["Encrypt"] = encryption_page

    decryption_page = Decryption_Page(
        master=main_window, width=window_width, height=window_height)
    page_collection["Decrypt"] = decryption_page

    show_page(page_to_show=start_page)


def show_page(current_page=None, page_to_show="Options"):
    if current_page:
        current_page.hide()

    page_collection[page_to_show].show()


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.page_width = kwargs["width"]
        self.page_height = kwargs["height"]

        self.pack_forget()

    def show(self):
        self.pack(side="top", fill="both", expand=True)

    def hide(self):
        self.pack_forget()


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
                                text="Encrypt", command=lambda: show_page(current_page=self, page_to_show="Encrypt"), font=("Arial", 15), border=6, borderwidth=6)
        btn_encrypt.pack(pady=20)

        frm_btn_decrypt = tk.Frame(
            master=frm_btn, relief=tk.RAISED, borderwidth=0)
        frm_btn_decrypt.grid(row=0, column=1)
        btn_decrypt = tk.Button(master=frm_btn_decrypt,
                                text="Decrypt", command=lambda: show_page(current_page=self, page_to_show="Decrypt"), font=("Arial", 15), border=6, borderwidth=6)
        btn_decrypt.pack(pady=20)


class Encryption_Page(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        frm_backbutton = tk.Frame(master=self, relief=tk.RAISED, borderwidth=0)
        frm_backbutton.place(relx=0, rely=0, anchor="nw")

        btn_back = tk.Button(master=frm_backbutton, text="Back",
                             command=lambda: show_page(self, "Options"), font=("Arial", 10, 'bold'), border=6, borderwidth=6)
        btn_back.pack()

        rows = 3
        first_row_height = int(self.page_height/6)
        row_height = int((self.page_height - first_row_height)/rows)
        column_width = int(self.page_width)
        self.rowconfigure(0, minsize=first_row_height)
        self.rowconfigure([1, 2, 3], minsize=row_height)
        self.columnconfigure(0, minsize=column_width)

        frm_createpassword = tk.Frame(
            master=self, relief=tk.FLAT, borderwidth=0)
        frm_createpassword.grid(row=1, column=0)
        frm_createpassword.rowconfigure(0, minsize=row_height)
        frm_createpassword.columnconfigure([0, 1], minsize=int(column_width/2))

        lbl_createpassword = tk.Label(
            master=frm_createpassword, text="Create Password:", fg="grey", font=("Arial", 12, 'bold'))
        lbl_createpassword.grid(row=0, column=0, sticky="w", padx=2)
        ent_createpassword = tk.Entry(
            master=frm_createpassword, width=15, font=("Arial", 12), show="*", borderwidth=2)
        ent_createpassword.grid(row=0, column=1, sticky="e", padx=(10, 10))

        frm_confirmpassword = tk.Frame(
            master=self, relief=tk.FLAT, borderwidth=0)
        frm_confirmpassword.grid(row=2, column=0)
        frm_confirmpassword.rowconfigure(0, minsize=row_height)
        frm_confirmpassword.columnconfigure(
            [0, 1], minsize=int(column_width/2))

        lbl_confirmpassword = tk.Label(
            master=frm_confirmpassword, text="Confirm Password:", fg="grey", font=("Arial", 12, 'bold'))
        lbl_confirmpassword.grid(row=0, column=0, sticky="w", padx=2)

        ent_confirmpassword = tk.Entry(
            master=frm_confirmpassword, width=15, font=("Arial", 12), show="*", borderwidth=2)
        ent_confirmpassword.grid(row=0, column=1, sticky="e", padx=(10, 10))

        frm_btn_encrypt = tk.Frame(master=self, relief=tk.FLAT, borderwidth=0)
        frm_btn_encrypt.grid(row=3, column=0)

        btn_encrypt = tk.Button(master=frm_btn_encrypt,
                                relief=tk.RAISED, border=6, borderwidth=6, text="Encrypt", font=("Arial", 12, "bold"))
        btn_encrypt.pack(pady=(0, 10))


class Decryption_Page(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        frm_backbutton = tk.Frame(master=self, relief=tk.RAISED, borderwidth=0)
        frm_backbutton.place(relx=0, rely=0, anchor="nw")

        btn_back = tk.Button(master=frm_backbutton, text="Back",
                             command=lambda: show_page(self, "Options"), font=("Arial", 10, 'bold'), border=6, borderwidth=6)
        btn_back.pack()

        frm_enterpassword = tk.Frame(
            master=self, relief=tk.FLAT, borderwidth=0)
        frm_enterpassword.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        lbl_enterpassword = tk.Label(
            master=frm_enterpassword, text="Enter Password:", font=("Arial", 12, 'bold'), fg="grey")
        lbl_enterpassword.pack(side=tk.LEFT, padx=(0, 10))

        ent_enterpassword = tk.Entry(master=frm_enterpassword, width=15, font=(
            "Arial", 12), show="*", borderwidth=2)
        ent_enterpassword.pack(side=tk.RIGHT, padx=(10, 0))

        frm_btn_decrypt = tk.Frame(master=self, relief=tk.FLAT, borderwidth=0)
        frm_btn_decrypt.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        btn_decrypt = tk.Button(master=frm_btn_decrypt,
                                relief=tk.RAISED, border=6, borderwidth=6, text="Decrypt", font=("Arial", 12, "bold"))
        btn_decrypt.pack(pady=(0, 10))
