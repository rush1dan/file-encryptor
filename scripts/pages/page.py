import tkinter as tk


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