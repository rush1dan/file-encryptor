import tkinter as tk
from pages.page import Page
from pages.options_page import Options_Page
from pages.encryption_page import Encryption_Page
from pages.decryption_page import Decryption_Page
from pages.progress_page import Progress_Page
from pages.complete_page import Complete_Page


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

