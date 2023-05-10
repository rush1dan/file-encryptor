import tkinter as tk
from tkinter import messagebox
from pages.page import Page
from data import Data
import utils
import threading
from encryptor import Encryptor
from traceback import print_exc as print_error

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
        frm_processtitle.place(relx=0.5, rely=0.05, anchor="n")

        lbl_processtitle = tk.Label(
            master=frm_processtitle, text="Encrypt File(s)", font=("Arial", int(15 * Data.SCREEN_RES_FACTOR), 'bold'))
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
            master=frm_createpassword, text="Create Password:", fg="grey", font=("Arial", int(12 * Data.SCREEN_RES_FACTOR), 'bold'),
            anchor="e", justify="right")
        lbl_createpassword.grid(row=0, column=0, sticky="e", padx=int(2 * Data.SCREEN_RES_FACTOR))

        self.ent_createpassword = tk.Entry(
            master=frm_createpassword, width=15, font=("Arial", int(12 * Data.SCREEN_RES_FACTOR)), show="*", borderwidth=int(2 * Data.SCREEN_RES_FACTOR))
        self.ent_createpassword.grid(
            row=0, column=1, sticky="w", padx=(int(10 * Data.SCREEN_RES_FACTOR), int(10 * Data.SCREEN_RES_FACTOR)))

        frm_confirmpassword = tk.Frame(
            master=self, relief=tk.FLAT, borderwidth=0)
        frm_confirmpassword.grid(row=2, column=0)
        frm_confirmpassword.rowconfigure(0, minsize=row_height)
        frm_confirmpassword.columnconfigure(
            [0, 1], minsize=int(column_width/2))

        lbl_confirmpassword = tk.Label(
            master=frm_confirmpassword, text="Confirm Password:", fg="grey", font=("Arial", int(12 * Data.SCREEN_RES_FACTOR), 'bold'),
            anchor="e", justify="right")
        lbl_confirmpassword.grid(row=0, column=0, sticky="e", padx=int(2 * Data.SCREEN_RES_FACTOR))

        self.ent_confirmpassword = tk.Entry(
            master=frm_confirmpassword, width=15, font=("Arial", int(12 * Data.SCREEN_RES_FACTOR)), show="*", 
            borderwidth=int(2 * Data.SCREEN_RES_FACTOR))
        self.ent_confirmpassword.grid(
            row=0, column=1, sticky="w", padx=(int(10 * Data.SCREEN_RES_FACTOR), int(10 * Data.SCREEN_RES_FACTOR)))

        frm_btn_encrypt = tk.Frame(master=self, relief=tk.FLAT, borderwidth=0)
        frm_btn_encrypt.grid(row=3, column=0)

        btn_encrypt = tk.Button(master=frm_btn_encrypt,
                                relief=tk.RAISED, border=int(6 * Data.SCREEN_RES_FACTOR), borderwidth=int(6 * Data.SCREEN_RES_FACTOR), text="Encrypt", font=("Arial", int(12 * Data.SCREEN_RES_FACTOR), "bold"),
                                command=self.encryption_process)
        btn_encrypt.pack(pady=(0, int(10 * Data.SCREEN_RES_FACTOR)))

        self.master.bind('<Return>', self.on_pressed_enter)


        super().show()

    def on_pressed_enter(self, event):
        from page_utils import get_current_page

        if get_current_page() == self:
            self.encryption_process()
   
    def on_error(self, error_title: str, error_msg: str, hide_mainwindow: bool = True):
        from page_utils import hide_main_window, close_main_window

        if hide_mainwindow:
            hide_main_window()
        messagebox.showerror(title=error_title, message=error_msg)
        if hide_mainwindow:
            close_main_window()

    def show_info(self, info_title: str, info_msg: str, hide_mainwindow: bool = False):
        from page_utils import hide_main_window, close_main_window

        if hide_mainwindow:
            hide_main_window()
        messagebox.showinfo(title=info_title, message=info_msg)
        if hide_mainwindow:
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

        encryptable_folders = []
        encryptable_files = []
        total_encryptable_file_count = 0

        for file in Data.selected_files:
            encryptable_files.append(file)
            total_encryptable_file_count += 1
        
        for folder in Data.selected_folders:
            encryptable_files_in_folder = utils.get_all_files_under_directory(folder)
            encryptable_filecount_in_folder = len(encryptable_files_in_folder)
            if encryptable_filecount_in_folder > 0:
                encryptable_folders.append(folder)
                total_encryptable_file_count += encryptable_filecount_in_folder

        if total_encryptable_file_count == 0:
            self.show_info(info_title="", info_msg="Nothing to encrypt.", hide_mainwindow=True)
            return 

        try:
            from page_utils import save_filesorfolders_at

            suggested_directory = utils.get_parent_directory(Data.selected_files[0] if len(Data.selected_files) > 0 else Data.selected_folders[0])
            saving_directory = save_filesorfolders_at(suggested_directory)

            if saving_directory:
                self.encrypt_files_and_folders(encryptable_files, encryptable_folders, total_encryptable_file_count, created_password, saving_directory)

        except Exception as ex:
            print_error()
            self.on_error(type(ex).__name__, str(ex))
            return
        
    def encrypt_files_and_folders(self, encryptable_files: list[str], encryptable_folders: list[str], total_encryptable_file_count: int, 
                                  created_password: str, saving_directory: str):
            from page_utils import show_progress, show_updated_progress, show_completion

            show_progress(total_file_count=total_encryptable_file_count)

            def encrypt_folders_after_files(already_encrypted_file_count: int):
                if already_encrypted_file_count < total_encryptable_file_count:
                    Encryptor.encrypt_folders(encryptable_folders, created_password, saving_directory,
                                            lambda files_index, file_in_process: show_updated_progress(files_index, file_in_process),
                                            lambda files_processed: print(f"{files_processed} files encrypted"),
                                            lambda folder_count: show_completion(folder_count),
                                            lambda error_title, error_msg: self.on_error(error_title, error_msg))
                else:
                    show_completion(already_encrypted_file_count)

            if len(encryptable_files) > 0:
                new_thread = threading.Thread(target=Encryptor.encrypt_files, args=(encryptable_files, created_password, saving_directory, True, 
                    lambda files_index, file_in_process: show_updated_progress(files_index, file_in_process),
                    lambda files_processed: print(f"{files_processed} files encrypted"),
                    lambda file_count: encrypt_folders_after_files(file_count),
                    lambda error_title, error_msg: self.on_error(error_title, error_msg)), daemon=True)
                new_thread.start()
            elif len(encryptable_folders) > 0:
                new_thread = threading.Thread(target=Encryptor.encrypt_folders, args=(encryptable_folders, created_password, saving_directory, 
                    lambda files_index, file_in_process: show_updated_progress(files_index, file_in_process),
                    lambda files_processed: print(f"{files_processed} files encrypted"),
                    lambda folder_count: show_completion(folder_count),
                    lambda error_title, error_msg: self.on_error(error_title, error_msg)), daemon=True)
                new_thread.start()

