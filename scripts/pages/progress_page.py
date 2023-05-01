import tkinter as tk
from pages.page import Page
from data import Data


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

        self.process_type = "Encrypt"

        match Data.operation_mode:
            case Data.OperationMode.ENCRYPTION:
                self.process_type = "Encrypt"
            case Data.OperationMode.DECRYPTION:
                self.process_type = "Decrypt"
            case _:
                print("Operation mode argument not passed properly.")
        
        initial_file_count = self.processed_filecount+1
        self.process_label = tk.Label(master=frm_processlabel, 
            text=f"{self.process_type}ing Files ({initial_file_count}/{self.total_files_for_processing})",
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
            self.process_label.config(text="{process}ing files {files_encrypting}/{total_files}".format(process=self.process_type,
                files_encrypting=self.processed_filecount+1, 
                total_files=self.total_files_for_processing))
            self.processingfile_label.config(text=self.files_in_progress[self.processed_filecount])

    def set_progress_finished(self):
        self.progress_finished = True
