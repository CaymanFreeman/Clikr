import multiprocessing
import sys

import customtkinter

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
        self.title("Easy Auto Clicker")
        self.resizable(width=False, height=False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        click_length_frame = ClickLengthFrame(master=self)
        click_length_frame.grid(row=0, column=0, padx=FRAME_PADDING, pady=FRAME_PADDING, sticky="ew")

        interval_frame = ClickIntervalFrame(master=self)
        interval_frame.grid(row=1, column=0, padx=FRAME_PADDING, pady=FRAME_PADDING, sticky="ew")

        click_style_frame = ClickStyleFrame(master=self)
        click_style_frame.grid(row=2, column=0, padx=FRAME_PADDING, pady=FRAME_PADDING, sticky="ew")

        location_frame = LocationFrame(master=self)
        location_frame.grid(row=3, column=0, padx=FRAME_PADDING, pady=FRAME_PADDING, sticky="ew")

        start_stop_frame = StartStopFrame(master=self)
        start_stop_frame.grid(row=5, column=0, padx=FRAME_PADDING, pady=FRAME_PADDING, sticky="ew")

        hotkey_frame = HotkeyFrame(master=self, start_stop_frame=start_stop_frame)
        hotkey_frame.grid(row=4, column=0, padx=FRAME_PADDING, pady=FRAME_PADDING, sticky="ew")

        self.update()


if __name__ == "__main__":
    if sys.platform.startswith('win'):
        multiprocessing.freeze_support()
    customtkinter.set_appearance_mode("dark")
    app = App()
    app.mainloop()
