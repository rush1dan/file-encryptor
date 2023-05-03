from page_manager import Page_Manager
from tkinter import filedialog


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

def hide_main_window():
    Page_Manager.hide_main_window()

def close_main_window():
    Page_Manager.close_main_window()

def get_current_page():
    return Page_Manager.current_page