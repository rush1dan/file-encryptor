import tkinter as tk
from pages.page import Page
from data import Data
from PIL import Image, ImageTk
import base64
import io


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
