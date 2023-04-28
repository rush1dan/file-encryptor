import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from encryptor import Encryptor
from decryptor import Decryptor
import utils
from data import Data
import threading
from PIL import Image, ImageTk
import base64
import io

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.page_width = kwargs["width"]
        self.page_height = kwargs["height"]

        self.pack_forget()

    def show(self):
        self.pack(side="top", fill="both", expand=True)
        self.primary_focus()

    def hide(self):
        self.pack_forget()

    def clear_entry(self):
        pass

    def primary_focus(self):
        pass

    def on_error(self, error_title: str, error_msg: str):
        pass

    def show_info(self, info_title: str, info_msg: str, hide_mainwindow: bool):
        pass

class Page_Manager:
    page_collection = {}
    current_page = None
    main_window = None

    @classmethod
    def setup_all_pages(cls, main_window: tk.Widget, window_width: int, window_height: int, start_page: str):
        cls.main_window = main_window

        options_page = Options_Page(master=main_window, width=window_width, height=window_height)
        cls.page_collection["Options"] = options_page

        encryption_page = Encryption_Page(master=main_window, width=window_width, height=window_height)
        cls.page_collection["Encrypt"] = encryption_page

        decryption_page = Decryption_Page(master=main_window, width=window_width, height=window_height)
        cls.page_collection["Decrypt"] = decryption_page

        progress_page = Progress_Page(master=main_window, width=window_width, height=window_height)
        cls.page_collection["Progress"] = progress_page

        complete_page = Complete_Page(master=main_window, width=window_width, height=window_height)
        cls.page_collection["Complete"] = complete_page

        cls.show_page(page_to_show=start_page)

    @classmethod
    def show_page(cls, page_to_show="Options") -> Page:
        if cls.current_page:
            cls.current_page.clear_entry()
            cls.current_page.hide()

        page = cls.page_collection[page_to_show]
        cls.current_page = page
        page.show()
        return page

    @classmethod
    def hide_main_window(cls):
        if cls.main_window:
            cls.main_window.withdraw()

    @classmethod
    def close_main_window(cls):
        if cls.main_window:
            cls.main_window.destroy()

class Options_Page(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
    

    def show(self):
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
                                text="Encrypt", command=lambda: Page_Manager.show_page(page_to_show="Encrypt"), font=("Arial", 15), border=6, borderwidth=6)
        btn_encrypt.pack(pady=20)

        frm_btn_decrypt = tk.Frame(
            master=frm_btn, relief=tk.RAISED, borderwidth=0)
        frm_btn_decrypt.grid(row=0, column=1)
        btn_decrypt = tk.Button(master=frm_btn_decrypt,
                                text="Decrypt", command=lambda: Page_Manager.show_page(page_to_show="Decrypt"), font=("Arial", 15), border=6, borderwidth=6)
        btn_decrypt.pack(pady=20)


        super().show()


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


        super().show()

    def on_error(self, error_title: str, error_msg: str):
        Page_Manager.hide_main_window()
        messagebox.showerror(title=error_title, message=error_msg)
        Page_Manager.close_main_window()

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

        match Data.operation_object:
            case Data.OperationObject.FILE:
                selected_files = Data.selected_files_or_folders
                encryptable_files = selected_files
                encryptable_file_count = len(encryptable_files)
                if encryptable_file_count == 0:
                    self.show_info(info_title="", info_msg="Nothing to encrypt.", hide_mainwindow=True)
                    return 

            case Data.OperationObject.FOLDER:
                selected_files_list_list = [utils.get_all_files_under_directory(folder) for folder in Data.selected_files_or_folders]
                selected_files = []
                for files_list in selected_files_list_list:
                    selected_files.extend(files_list)
                encryptable_files = selected_files
                encryptable_file_count = len(encryptable_files)
                if encryptable_file_count == 0:
                    self.show_info(info_title="", info_msg="Nothing to decrypt.", hide_mainwindow=True)
                    return 

            case _:
                print("Operation object argument not passed properly. Decryption aborted.")

        try:
            suggested_directory = utils.get_parent_directory(Data.selected_files_or_folders[0])
            saving_directory = save_filesorfolders_at(suggested_directory)

            if saving_directory:
                match Data.operation_object:
                    case Data.OperationObject.FILE:
                        set_files_in_progress(encryptable_files)
                        show_progress(total_file_count=encryptable_file_count)

                        new_thread = threading.Thread(target=Encryptor.encrypt_files, args=(encryptable_files, created_password, saving_directory, True, 
                            lambda files_processed: show_updated_progress(files_processed),
                            lambda file_count: show_completion(file_count),
                            lambda error_title, error_msg: self.on_error(error_title, error_msg)), daemon=True)
                        new_thread.start()

                    case Data.OperationObject.FOLDER:
                        set_files_in_progress(encryptable_files)
                        show_progress(total_file_count=encryptable_file_count)

                        new_thread = threading.Thread(target=Encryptor.encrypt_folders, args=(Data.selected_files_or_folders, created_password, saving_directory, 
                            lambda files_processed: show_updated_progress(files_processed),
                            lambda file_count: show_completion(file_count),
                            lambda error_title, error_msg: self.on_error(error_title, error_msg)), daemon=True)
                        new_thread.start()
                        
                    case _:
                        print("Operation object argument not passed properly. Encryption aborted.")

        except FileNotFoundError:
            print("No File Argument")


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
            master=frm_processtitle, text="Decrypt File(s)", font=("Arial", 15, 'bold'))
        lbl_processtitle.pack()

        frm_enterpassword = tk.Frame(
            master=self, relief=tk.FLAT, borderwidth=0)
        frm_enterpassword.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        lbl_enterpassword = tk.Label(
            master=frm_enterpassword, text="Enter Password:", font=("Arial", 12, 'bold'), fg="grey")
        lbl_enterpassword.pack(side=tk.LEFT, padx=(0, 10))

        self.ent_enterpassword = tk.Entry(master=frm_enterpassword, width=15, font=(
            "Arial", 12), show="*", borderwidth=2)
        self.ent_enterpassword.focus_set()
        self.ent_enterpassword.pack(side=tk.RIGHT, padx=(10, 0))

        frm_btn_decrypt = tk.Frame(master=self, relief=tk.FLAT, borderwidth=0)
        frm_btn_decrypt.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        btn_decrypt = tk.Button(master=frm_btn_decrypt,
                                relief=tk.RAISED, border=6, borderwidth=6, text="Decrypt", font=("Arial", 12, "bold"),
                                command=self.decryption_process)
        btn_decrypt.pack(pady=(0, 0))


        super().show()

    def on_error(self, error_title: str, error_msg: str):
        Page_Manager.hide_main_window()
        messagebox.showerror(title=error_title, message=error_msg)
        Page_Manager.close_main_window()

    def show_info(self, info_title: str, info_msg: str, hide_mainwindow: bool):
        if hide_mainwindow:
            Page_Manager.hide_main_window()
        messagebox.showinfo(title=info_title, message=info_msg)
        if hide_mainwindow:
            Page_Manager.close_main_window()

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

        decryptable_files = []
        decryptable_file_count = 0

        match Data.operation_object:
            case Data.OperationObject.FILE:
                selected_files = Data.selected_files_or_folders
                decryptable_files = [file for file in selected_files if utils.get_file_extension(file) == ".enc"]
                decryptable_file_count = len(decryptable_files)
                if decryptable_file_count == 0:
                    self.show_info(info_title="", info_msg="Nothing to decrypt.", hide_mainwindow=True)
                    return 

            case Data.OperationObject.FOLDER:
                selected_files_list_list = [utils.get_all_files_under_directory(folder) for folder in Data.selected_files_or_folders]
                selected_files = []
                for files_list in selected_files_list_list:
                    selected_files.extend(files_list)
                decryptable_files = [file for file in selected_files if utils.get_file_extension(file) == ".enc"]
                decryptable_file_count = len(decryptable_files)
                if decryptable_file_count == 0:
                    self.show_info(info_title="", info_msg="Nothing to decrypt.", hide_mainwindow=True)
                    return 

            case _:
                print("Operation object argument not passed properly. Decryption aborted.")

        try:
            suggested_directory = utils.get_parent_directory(Data.selected_files_or_folders[0])
            saving_directory = save_filesorfolders_at(suggested_directory)

            if saving_directory:
                match Data.operation_object:              
                    case Data.OperationObject.FILE:
                        set_files_in_progress(decryptable_files)
                        show_progress(total_file_count=decryptable_file_count)

                        new_thread = threading.Thread(target=Decryptor.decrypt_files, args=(decryptable_files, entered_password, saving_directory, 
                            lambda files_processed: show_updated_progress(files_processed),
                            lambda file_count: show_completion(file_count),
                            lambda error_title, error_msg: self.on_error(error_title, error_msg)), daemon=True)
                        new_thread.start()

                    case Data.OperationObject.FOLDER:
                        set_files_in_progress(decryptable_files)
                        show_progress(total_file_count=decryptable_file_count)

                        new_thread = threading.Thread(target=Decryptor.decrypt_folders, args=(Data.selected_files_or_folders, entered_password, saving_directory, 
                            lambda files_processed: show_updated_progress(files_processed),
                            lambda file_count: show_completion(file_count),
                            lambda error_title, error_msg: self.on_error(error_title, error_msg)), daemon=True)
                        new_thread.start()

                    case _:
                        print("Operation object argument not passed properly. Decryption aborted.")

        except FileNotFoundError:
            print("No File Argument")

class Progress_Page(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        
        self.files_in_progress = []
        self.processed_filecount = 0
        self.total_files_for_processing = 0
        self.progress_finished = False

    def show(self):
        application_window = self.master

        screenWidth = application_window.winfo_screenwidth()
        screenHeight = application_window.winfo_screenheight()
        screenAspectRatio = screenWidth / screenHeight

        windowAspectRatio = 5
        windowWidth = int(screenWidth / 5)
        windowHeight = int(windowWidth / windowAspectRatio)

        self.center_window(windowWidth, windowHeight)

        row0_height= int(windowHeight * 0.6)
        row1_height = int(windowHeight * 0.4)

        self.rowconfigure(0, minsize=row0_height)   
        self.rowconfigure(1, minsize=row1_height)     
        self.columnconfigure(0, minsize=windowWidth)

        frm_process = tk.Frame(master=self, relief=tk.FLAT, borderwidth=0)
        frm_process.grid(row=0, column=0, pady=(int(row0_height/4), 0), sticky="n")

        frm_process.columnconfigure(0, minsize=int(windowWidth * 2.1 / 3))
        frm_process.columnconfigure(1, minsize=int(windowWidth * 0.9 / 3))

        frm_file = tk.Frame(master=self, relief=tk.FLAT, borderwidth=0)
        frm_file.grid(row=1, column=0, pady=(0, int(row1_height/4)), sticky="s")

        frm_processlabel = tk.Frame(master=frm_process, relief=tk.FLAT, borderwidth=0)
        frm_processlabel.grid(row=0, column=0, sticky="e")

        process_type = "Encrypt"

        match Data.operation_mode:
            case Data.OperationMode.ENCRYPTION:
                process_type = "Encrypt"
            case Data.OperationMode.DECRYPTION:
                process_type = "Decrypt"
            case _:
                print("Operation mode argument not passed properly.")
        
        initial_file_count = self.processed_filecount+1
        self.process_label = tk.Label(master=frm_processlabel, 
            text=f"{process_type}ing Files ({initial_file_count}/{self.total_files_for_processing})",
            font=("Arial", 15))
        self.process_label.pack(side="right")

        frm_dotprogresslabel = tk.Frame(master=frm_process, relief=tk.FLAT, borderwidth=0)
        frm_dotprogresslabel.grid(row=0, column=1, sticky="w")

        self.dotprogress_label = tk.Label(master=frm_dotprogresslabel, text="", font=("Arial", 15, "bold"))
        self.dotprogress_label.pack(side="left")

        initial_file_index = 0
        self.processingfile_label = tk.Label(master=frm_file, text=self.files_in_progress[initial_file_index], font=("Arial", 8),
            wraplength=windowWidth - 10, justify="center")
        self.processingfile_label.pack()

        self.animate_label(self.dotprogress_label, "")


        super().show()

    def center_window(self, width=300, height=200):
        # get screen width and height
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # calculate position x and y coordinates
        x = int((screen_width/2)) - int((width/2))
        y = int((screen_height/2)) - int((height/2))
        self.master.geometry(f'{width}x{height}+{x}+{y}')
        self.master.resizable(0, 0)

    def animate_label(self, label: tk.Label, dots: str):
        dots += ". "
        if len(dots) > 6:
            dots = ""
        label.config(text=dots)
        if not self.progress_finished:
            self.master.after(500, lambda: self.animate_label(label, dots))

    def set_files_in_progress(self, files: list):
        self.files_in_progress = files

    def set_total_files_for_processing(self, file_count: int):
        self.total_files_for_processing = file_count

    def set_updated_progress(self, files_processed: int):
        self.processed_filecount = files_processed
        if self.processed_filecount < self.total_files_for_processing:
            self.process_label.config(text="Encrypting files {files_encrypting}/{total_files}".format(files_encrypting=self.processed_filecount+1, 
                total_files=self.total_files_for_processing))
            self.processingfile_label.config(text=self.files_in_progress[self.processed_filecount])

    def set_progress_finished(self):
        self.progress_finished = True

class Complete_Page(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

    def show(self):
        application_window = self.master

        screenWidth = application_window.winfo_screenwidth()
        screenHeight = application_window.winfo_screenheight()
        screenAspectRatio = screenWidth / screenHeight

        windowAspectRatio = 3
        windowWidth = int(screenWidth / 7)
        windowHeight = int(windowWidth / windowAspectRatio)

        self.center_window(windowWidth, windowHeight)

        self.rowconfigure(0, minsize=int(windowHeight))
        self.columnconfigure(0, minsize=int(windowWidth * 0.9 / 3))
        self.columnconfigure(1, minsize=int(windowWidth * 2.1 / 3))

        process_type = "Encrypt"

        match Data.operation_mode:
            case Data.OperationMode.ENCRYPTION:
                process_type = "Encrypt"
            case Data.OperationMode.DECRYPTION:
                process_type = "Decrypt"
            case _:
                print("Operation mode argument not passed properly.")

        frm_completion_icon = tk.Frame(master=self, relief=tk.FLAT, borderwidth=0)
        frm_completion_icon.grid(row=0, column=0, sticky="e")

        icon_dimension = int(windowHeight/2)
        right_padding = int(icon_dimension/3.5)
        #from https://www.motobit.com/util/base64-decoder-encoder.asp, 32*32 png to utf-8 base64 string
        base64_png = "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIxSURBVFhHxZdJTtxAFIYf7JoNSKwiMUqQNYM4AIMiEDlBuEIklHvABSKGS8AWLsAghgVSEMM6IQqLAAJUzf/72ea124VHxP/pteyqcv2vbVe5qkPyqindiK84mpYOGcPxMI67gzqRW8QV4hCxi/otBMtqkJPPiA3EHUzzwbZONoNrS8tJA7GKeDJdF8PJY9BHU7rCXnPKySjiNO6oKuyLfeaSkwnEb3N5PbBPJ+Ohi0f6z+s3j9AkPHdCn3l9t92HPo5G6GqkL0utdAJ7HkOvFulQK/+2pzALDsAnYMsD6NUyRDnObYOK0PwOUGfAk8SGmnOGKzLJZGDNI/FOtD0O9cRM6mQpLqxImvl/wHLbLsbJNyawZopKMwcKmRN642ffFJWilLmyxwRuTEEbvcCeJ0kzfwAst+1ScfKHCTybohYmwQ34Dmx5hM98Adh2XujtS2AK/AWUA8vA1lc2J2ECbY+AQ+YIWDGJH4D1tZiT8BGkvoRD4BIk9RPUYq4EL6F3GA6CC/CWKpjHw/DNiWgAnIM0VTInwUSUYyruB8kk7kFF83AqpnJ8jPrALxCZzwNbX5j4Y0Tp5/jRVKfCJI7BF2DLC6OL1cSK2cmKaeLFu8goAr3a9OFLMsrJCOK9F6UjoZtHXDq/RxJqnrEsj6R34sRcXg297Rn/PKnXrVnm6PCib/tK0Fdp6RBdRxTdnHJDm7k5Lbo9X8TRTLg9H8JxT1An8g9xjeD2fAf12/m25yIv3HMemvUOfcwAAAAASUVORK5CYII="
        img_data_bytes = base64.b64decode(base64_png)
        img = Image.open(io.BytesIO(img_data_bytes))
        img_resized = img.resize((icon_dimension, icon_dimension))
        completion_icon = ImageTk.PhotoImage(img_resized)
        lbl_completion_icon = tk.Label(master=frm_completion_icon, image=completion_icon, compound="right")
        lbl_completion_icon.pack(side="right", padx=(0, right_padding))
        lbl_completion_icon.image = completion_icon

        frm_completion_text = tk.Frame(master=self, relief=tk.FLAT, borderwidth=0)
        frm_completion_text.grid(row=0, column=1, sticky="w")

        lbl_completion_text = tk.Label(master=frm_completion_text, text=f"{process_type}ion Complete", font=("Arial", 13, "bold"))
        lbl_completion_text.pack(side="left")


        super().show()

    def center_window(self, width=300, height=200):
        # get screen width and height
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # calculate position x and y coordinates
        x = int((screen_width/2)) - int((width/2))
        y = int((screen_height/2)) - int((height/2))
        self.master.geometry(f'{width}x{height}+{x}+{y}')
        self.master.resizable(0, 0)

def show_progress(total_file_count: int):
    progress_page = Page_Manager.page_collection["Progress"]
    progress_page.set_total_files_for_processing(total_file_count)
    
    Page_Manager.show_page("Progress")

def show_updated_progress(files_processed: int):
    progress_page = Page_Manager.page_collection["Progress"]
    progress_page.set_updated_progress(files_processed)

def set_files_in_progress(filepaths: list[str]):
    progress_page = Page_Manager.page_collection["Progress"]
    progress_page.set_files_in_progress(filepaths)

def show_completion(total_file_count: int):
    Page_Manager.page_collection["Progress"].set_progress_finished()
    Page_Manager.show_page("Complete")
    
def save_file(content: bytes, defaultextension: str, filetypes: tuple, suggested_path=None, suggested_filename=None, 
              on_saving_initiated=None, on_file_saved=None, on_cancelled=None):
    file = filedialog.asksaveasfilename(title="Save As", initialdir=suggested_path if suggested_path != None else ".", 
                                        initialfile=suggested_filename if suggested_filename != None else "", 
                                        defaultextension=defaultextension, filetypes=filetypes)

    if file:
        if on_saving_initiated != None:
            on_saving_initiated()

    try:
        with open(file, "wb") as f:
            f.write(content)

        if on_file_saved != None:
            on_file_saved()
    except FileNotFoundError:
        print("No File Path Selected")
        if on_cancelled != None:
            on_cancelled()

def save_filesorfolders_at(suggested_dir: str)->str:
    return filedialog.askdirectory(initialdir=suggested_dir, mustexist=True)

