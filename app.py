import multiprocessing
import os.path
import sys

import customtkinter

from appearance_frame import AppearanceFrame
from click_length_frame import ClickLengthFrame
from click_style_frame import ClickStyleFrame
from constants import *
from hotkey_frame import HotkeyFrame
from interval_frame import ClickIntervalFrame
from location_frame import LocationFrame
from start_stop_frame import StartStopFrame


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme(os.path.join("assets", "easy_auto_clicker_theme.json"))

        self.title("Easy Auto Clicker")
        self.iconbitmap(os.path.join("assets", "icon.ico"))
        self.resizable(width=False, height=False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        appearance_frame = AppearanceFrame(master=self)
        appearance_frame.grid(row=0, column=0, padx=FRAME_PADDING, pady=FRAME_PADDING, sticky="ew")

        click_length_frame = ClickLengthFrame(master=self)
        click_length_frame.grid(row=1, column=0, padx=FRAME_PADDING, pady=FRAME_PADDING, sticky="ew")

        interval_frame = ClickIntervalFrame(master=self)
        interval_frame.grid(row=2, column=0, padx=FRAME_PADDING, pady=FRAME_PADDING, sticky="ew")

        click_style_frame = ClickStyleFrame(master=self)
        click_style_frame.grid(row=3, column=0, padx=FRAME_PADDING, pady=FRAME_PADDING, sticky="ew")

        location_frame = LocationFrame(master=self)
        location_frame.grid(row=4, column=0, padx=FRAME_PADDING, pady=FRAME_PADDING, sticky="ew")

        start_stop_frame = StartStopFrame(master=self)
        start_stop_frame.grid(row=6, column=0, padx=FRAME_PADDING, pady=FRAME_PADDING, sticky="ew")

        hotkey_frame = HotkeyFrame(master=self, start_stop_frame=start_stop_frame)
        hotkey_frame.grid(row=5, column=0, padx=FRAME_PADDING, pady=FRAME_PADDING, sticky="ew")

        self.update()


if __name__ == "__main__":
    if sys.platform.startswith('win'):
        multiprocessing.freeze_support()
    app = App()
    app.mainloop()
