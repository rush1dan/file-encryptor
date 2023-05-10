import tkinter as tk
from tkinter import messagebox
from pages.page import Page
from data import Data
import utils
import threading
from decryptor import Decryptor
from traceback import print_exc as print_error


class Decryption_Page(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

    def show(self):
        # frm_backbutton = tk.Frame(master=self, relief=tk.RAISED, borderwidth=0)
        # frm_backbutton.place(relx=0, rely=0, anchor="nw")

        # btn_back = tk.Button(master=frm_backbutton, text="Back",
        #                      command=lambda: show_page(self, "Options"), font=("Arial", 10, 'bold'), border=6, borderwidth=6)
        # btn_back.pack()

        frm_processtitle = tk.Frame(master=self, relief=tk.FLAT, borderwidth=0)
        frm_processtitle.place(relx=0.5, rely=0.1, anchor="n")

        lbl_processtitle = tk.Label(
            master=frm_processtitle, text="Decrypt File(s)", font=("Arial", int(15 * Data.SCREEN_RES_FACTOR), 'bold'))
        lbl_processtitle.pack()

        frm_enterpassword = tk.Frame(
            master=self, relief=tk.FLAT, borderwidth=0)
        frm_enterpassword.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        lbl_enterpassword = tk.Label(
            master=frm_enterpassword, text="Enter Password:", font=("Arial", int(12 * Data.SCREEN_RES_FACTOR), 'bold'), fg="grey")
        lbl_enterpassword.pack(side=tk.LEFT, padx=(0, int(10 * Data.SCREEN_RES_FACTOR)))

        self.ent_enterpassword = tk.Entry(master=frm_enterpassword, width=15, font=(
            "Arial", int(12 * Data.SCREEN_RES_FACTOR)), show="*", borderwidth=int(2 * Data.SCREEN_RES_FACTOR))
        self.ent_enterpassword.focus_set()
        self.ent_enterpassword.pack(side=tk.RIGHT, padx=(int(10 * Data.SCREEN_RES_FACTOR), 0))

        frm_btn_decrypt = tk.Frame(master=self, relief=tk.FLAT, borderwidth=0)
        frm_btn_decrypt.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        btn_decrypt = tk.Button(master=frm_btn_decrypt,
                                relief=tk.RAISED, border=int(6 * Data.SCREEN_RES_FACTOR), borderwidth=int(6 * Data.SCREEN_RES_FACTOR), text="Decrypt", font=("Arial", int(12 * Data.SCREEN_RES_FACTOR), "bold"),
                                command=self.decryption_process)
        btn_decrypt.pack(pady=(0, 0))

        self.master.bind('<Return>', self.on_pressed_enter)


        super().show()

    def on_pressed_enter(self, event):
        from page_utils import get_current_page

        if get_current_page() == self:
            self.decryption_process()

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
        return self.ent_enterpassword.focus_set()

    def clear_entry(self):
        self.ent_enterpassword.delete(0, tk.END)

        self.ent_enterpassword.focus()

    def decryption_process(self):
        entered_password = self.ent_enterpassword.get()

        if len(entered_password) < 8:
            messagebox.showerror(title="Invalid Password Error",
                                 message="Invalid password entered.")
            return

        decryptable_folders = []
        decryptable_files = []
        total_decryptable_file_count = 0

        for file in Data.selected_files:
            if utils.get_file_extension(file) == ".enc":
                decryptable_files.append(file)
                total_decryptable_file_count += 1

        for folder in Data.selected_folders:
            decryptable_files_in_folder = utils.get_all_files_under_directory_with_extension(folder, ".enc")
            decryptable_filecount_in_folder = len(decryptable_files_in_folder)
            if decryptable_filecount_in_folder > 0:
                decryptable_folders.append(folder)
                total_decryptable_file_count += decryptable_filecount_in_folder

        if total_decryptable_file_count == 0:
                self.show_info(info_title="", info_msg="Nothing to decrypt.", hide_mainwindow=True)
                return

        try:
            from page_utils import save_filesorfolders_at

            suggested_directory = utils.get_parent_directory(Data.selected_files[0] if len(Data.selected_files) > 0 else Data.selected_folders[0])
            saving_directory = save_filesorfolders_at(suggested_directory)

            if saving_directory:
                self.decrypt_files_and_folders(decryptable_files, decryptable_folders, total_decryptable_file_count, entered_password, saving_directory)

        except Exception as ex:
            print_error()
            self.on_error(type(ex).__name__, str(ex))
            return
        
    def decrypt_files_and_folders(self, decryptable_files: list[str], decryptable_folders: list[str], total_decryptable_file_count: int, 
                                  entered_password: str, saving_directory: str):
        from page_utils import show_progress, show_updated_progress, show_completion

        show_progress(total_file_count=total_decryptable_file_count)

        def decrypt_folders_after_files(already_decrypted_file_count: int):
            if already_decrypted_file_count < total_decryptable_file_count:
                Decryptor.decrypt_folders(decryptable_folders, entered_password, saving_directory,
                                        lambda files_index, file_in_process: show_updated_progress(files_index, file_in_process),
                                        lambda files_processed: print(f"{files_processed} files decrypted"),
                                        lambda folder_count: show_completion(folder_count),
                                        lambda error_title, error_msg: self.on_error(error_title, error_msg, False))
            else:
                show_completion(already_decrypted_file_count)

        if len(decryptable_files) > 0:
            new_thread = threading.Thread(target=Decryptor.decrypt_files, args=(decryptable_files, entered_password, saving_directory, 
                lambda files_index, file_in_process: show_updated_progress(files_index, file_in_process),
                lambda files_processed: print(f"{files_processed} files decrypted"),
                lambda file_count: decrypt_folders_after_files(file_count),
                lambda error_title, error_msg: self.on_error(error_title, error_msg, False)), daemon=True)
            new_thread.start()
        elif len(decryptable_folders) > 0:
            new_thread = threading.Thread(target=Decryptor.decrypt_folders, args=(decryptable_folders, entered_password, saving_directory, 
                lambda files_index, file_in_process: show_updated_progress(files_index, file_in_process),
                lambda files_processed: print(f"{files_processed} files decrypted"),
                lambda folder_count: show_completion(folder_count),
                lambda error_title, error_msg: self.on_error(error_title, error_msg, False)), daemon=True)
            new_thread.start()
