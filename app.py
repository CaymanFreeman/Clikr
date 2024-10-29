import multiprocessing
import sys

import customtkinter

from appearance_frame import AppearanceFrame
from appearance_variables import AppearanceVariables
from click_length_frame import ClickLengthFrame
from click_style_frame import ClickStyleFrame
from config_handler import ConfigHandler, THEME_PATH, ICON_PATH
from hotkey_frame import HotkeyFrame
from interval_frame import ClickIntervalFrame
from label_variables import LabelVariables
from location_frame import LocationFrame
from start_stop_frame import StartStopFrame


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        ConfigHandler.initialize_config(self)
        label_variables = LabelVariables(self)
        self.protocol(name="WM_DELETE_WINDOW", func = lambda: ConfigHandler.save_config_and_exit(self))

        appearance_variables = AppearanceVariables()

        customtkinter.set_appearance_mode(self.getvar(name="APPEARANCE_MODE"))
        customtkinter.set_default_color_theme(THEME_PATH)

        self.title(label_variables.TITLE)
        self.iconbitmap(ICON_PATH)
        self.resizable(width=self.getvar(name="RESIZABLE_WIDTH"), height=self.getvar(name="RESIZABLE_HEIGHT"))

        frame_padding = self.getvar(name="FRAME_PADDING")

        self.appearance_frame = AppearanceFrame(master=self, label_variables=label_variables)
        self.appearance_frame.grid(row=0, column=0, padx=frame_padding, pady=frame_padding, sticky="ew")

        self.click_length_frame = ClickLengthFrame(master=self, label_variables=label_variables)
        self.click_length_frame.grid(row=1, column=0, padx=frame_padding, pady=frame_padding, sticky="ew")

        self.interval_frame = ClickIntervalFrame(master=self, label_variables=label_variables)
        self.interval_frame.grid(row=2, column=0, padx=frame_padding, pady=frame_padding, sticky="ew")

        self.click_style_frame = ClickStyleFrame(master=self, label_variables=label_variables)
        self.click_style_frame.grid(row=3, column=0, padx=frame_padding, pady=frame_padding, sticky="ew")

        self.location_frame = LocationFrame(master=self, appearance_variables=appearance_variables, label_variables=label_variables)
        self.location_frame.grid(row=4, column=0, padx=frame_padding, pady=frame_padding, sticky="ew")

        self.start_stop_frame = StartStopFrame(master=self, appearance_variables=appearance_variables, label_variables=label_variables)
        self.start_stop_frame.grid(row=6, column=0, padx=frame_padding, pady=frame_padding, sticky="ew")

        self.hotkey_frame = HotkeyFrame(master=self, start_stop_frame=self.start_stop_frame, appearance_variables=appearance_variables, label_variables=label_variables)
        self.hotkey_frame.grid(row=5, column=0, padx=frame_padding, pady=frame_padding, sticky="ew")

        self.update()


if __name__ == "__main__":
    if sys.platform.startswith('win'):
        multiprocessing.freeze_support()
    app = App()
    app.mainloop()
