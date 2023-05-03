import tkinter as tk
from tkinter import messagebox
from pages.page import Page
from data import Data
import utils
import threading
from encryptor import Encryptor


class Encryption_Page(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

    def show(self):
        # frm_backbutton = tk.Frame(master=self, relief=tk.RAISED, borderwidth=0)
        # frm_backbutton.place(relx=0, rely=0, anchor="nw")

        # btn_back = tk.Button(master=frm_backbutton, text="Back",
        #                      command=lambda: show_page(self, "Options"), font=("Arial", 10, 'bold'), border=6, borderwidth=6)
        # btn_back.pack()

        frm_processtitle = tk.Frame(master=self, relief=tk.FLAT, borderwidth=0)
        frm_processtitle.place(relx=0.5, rely=0.03, anchor="n")

        lbl_processtitle = tk.Label(
            master=frm_processtitle, text="Encrypt File(s)", font=("Arial", 15, 'bold'))
        lbl_processtitle.pack()

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

        self.ent_createpassword = tk.Entry(
            master=frm_createpassword, width=15, font=("Arial", 12), show="*", borderwidth=2)
        self.ent_createpassword.grid(
            row=0, column=1, sticky="e", padx=(10, 10))

        frm_confirmpassword = tk.Frame(
            master=self, relief=tk.FLAT, borderwidth=0)
        frm_confirmpassword.grid(row=2, column=0)
        frm_confirmpassword.rowconfigure(0, minsize=row_height)
        frm_confirmpassword.columnconfigure(
            [0, 1], minsize=int(column_width/2))

        lbl_confirmpassword = tk.Label(
            master=frm_confirmpassword, text="Confirm Password:", fg="grey", font=("Arial", 12, 'bold'))
        lbl_confirmpassword.grid(row=0, column=0, sticky="w", padx=2)

        self.ent_confirmpassword = tk.Entry(
            master=frm_confirmpassword, width=15, font=("Arial", 12), show="*", borderwidth=2)
        self.ent_confirmpassword.grid(
            row=0, column=1, sticky="e", padx=(10, 10))

        frm_btn_encrypt = tk.Frame(master=self, relief=tk.FLAT, borderwidth=0)
        frm_btn_encrypt.grid(row=3, column=0)

        btn_encrypt = tk.Button(master=frm_btn_encrypt,
                                relief=tk.RAISED, border=6, borderwidth=6, text="Encrypt", font=("Arial", 12, "bold"),
                                command=self.encryption_process)
        btn_encrypt.pack(pady=(0, 10))

        self.master.bind('<Return>', self.on_pressed_enter)


        super().show()

    def on_pressed_enter(self, event):
        from page_utils import get_current_page

        if get_current_page() == self:
            self.encryption_process()
   
    def on_error(self, error_title: str, error_msg: str):
        from page_utils import hide_main_window, close_main_window

        hide_main_window()
        messagebox.showerror(title=error_title, message=error_msg)
        close_main_window()

    def primary_focus(self):
        return self.ent_createpassword.focus_set()

    def clear_entry(self):
        self.ent_createpassword.delete(0, tk.END)
        self.ent_confirmpassword.delete(0, tk.END)

        self.ent_createpassword.focus()

    def encryption_process(self):
        created_password = self.ent_createpassword.get()
        confirmed_password = self.ent_confirmpassword.get()

        if len(created_password) < 8:
            messagebox.showerror(title="Password Strength Error",
                                 message="Password must be atleast 8 characters long.")
            return
        elif created_password != confirmed_password:
            messagebox.showerror(title="Password Mismatch Error",
                                 message="Password confirmation doesn't match.")
            return

        encryptable_files = []
        encryptable_file_count = 0

        if len(Data.selected_files) > 0:
            selected_files = Data.selected_files
            encryptable_files.extend(selected_files)
        
        if len(Data.selected_folders) > 0:
            selected_files_list_list = [utils.get_all_files_under_directory(folder) for folder in Data.selected_folders]
            selected_files = []
            for files_list in selected_files_list_list:
                selected_files.extend(files_list)
            encryptable_files.extend(selected_files)
        
        encryptable_file_count = len(encryptable_files)

        if encryptable_file_count == 0:
            self.show_info(info_title="", info_msg="Nothing to encrypt.", hide_mainwindow=True)
            return 

        def encrypt_files_and_folders(selected_files: list[str], selected_folders: list[str], total_encryptable_files: list[str],
                                      total_encryptable_file_count: int, saving_directory: str):
            set_files_in_progress(total_encryptable_files)
            show_progress(total_file_count=total_encryptable_file_count)

            def encrypt_folders_after_files(already_encrypted_file_count: int):
                if already_encrypted_file_count < total_encryptable_file_count:
                    Encryptor.encrypt_folders(selected_folders, created_password, saving_directory,
                                            lambda files_processed: show_updated_progress(files_processed + already_encrypted_file_count),
                                            lambda file_count: show_completion(file_count + already_encrypted_file_count),
                                            lambda error_title, error_msg: self.on_error(error_title, error_msg))
                else:
                    show_completion(already_encrypted_file_count)

            if len(selected_files) > 0:
                new_thread = threading.Thread(target=Encryptor.encrypt_files, args=(selected_files, created_password, saving_directory, True, 
                    lambda files_processed: show_updated_progress(files_processed),
                    lambda file_count: encrypt_folders_after_files(file_count),
                    lambda error_title, error_msg: self.on_error(error_title, error_msg)), daemon=True)
                new_thread.start()
            elif len(selected_folders) > 0:
                new_thread = threading.Thread(target=Encryptor.encrypt_folders, args=(selected_folders, created_password, saving_directory, 
                    lambda files_processed: show_updated_progress(files_processed),
                    lambda file_count: show_completion(file_count),
                    lambda error_title, error_msg: self.on_error(error_title, error_msg)), daemon=True)
                new_thread.start()

        try:
            from page_utils import save_filesorfolders_at, set_files_in_progress, show_progress, show_updated_progress, show_completion

            suggested_directory = utils.get_parent_directory(Data.selected_files[0] if len(Data.selected_files) > 0 else Data.selected_folders[0])
            saving_directory = save_filesorfolders_at(suggested_directory)

            if saving_directory:
                encrypt_files_and_folders(Data.selected_files, Data.selected_folders, encryptable_files, encryptable_file_count, saving_directory)

        except FileNotFoundError:
            print("No File Argument")

