import tkinter

import customtkinter

from config_handler import CLICK_LENGTH_LABEL, MILLISECONDS_CHOICE, MINUTES_CHOICE, HOURS_CHOICE, SECONDS_CHOICE
from integer_entry import IntegerEntry


class ClickLengthFrame(customtkinter.CTkFrame):

    def __init__(self, master: customtkinter.CTk):
        super().__init__(master)

        item_padding = master.getvar(name="ITEM_PADDING")

        self.grid_columnconfigure(index=1, weight=1)
        self.grid_columnconfigure(index=2, weight=1)

        self.grid_rowconfigure(index=0, weight=1)

        self.length_label = customtkinter.CTkLabel(self, text=CLICK_LENGTH_LABEL)
        self.length_label.grid(row=0, column=0, padx=item_padding, pady=item_padding, sticky="ew")

        self.length_entry = IntegerEntry(self, variable_name="CLICK_LENGTH", max_length=master.getvar(name="MAX_CLICK_INTERVAL_DIGITS"), min_value=master.getvar(name="MIN_CLICK_INTERVAL"))
        self.length_entry.grid(row=0, column=1, padx=item_padding, pady=item_padding, sticky="ew")

        self.length_timescale_dropdown = (customtkinter.CTkOptionMenu(self, values=[MILLISECONDS_CHOICE, SECONDS_CHOICE, MINUTES_CHOICE, HOURS_CHOICE], command=self.length_timescale_callback))
        self.length_timescale_dropdown.configure(variable=tkinter.StringVar(value=master.getvar(name="CLICK_LENGTH_SCALE")))
        self.length_timescale_dropdown.grid(row=0, column=2, padx=item_padding, pady=item_padding, sticky="ew")

    def length_timescale_callback(self, option_value) -> None:
        self.master.setvar(name="CLICK_LENGTH_SCALE", value=option_value)
