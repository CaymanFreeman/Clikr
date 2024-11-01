import tkinter

import customtkinter

from integer_entry import IntegerEntry
from language_handler import LanguageHandler
from variable_dropdown import VariableDropdown
from variable_label import VariableLabel


class ClickIntervalFrame(customtkinter.CTkFrame):

    def __init__(self, master: customtkinter.CTk, language_handler: LanguageHandler):
        super().__init__(master)
        self.language_handler = language_handler

        item_padding = master.getvar(name="ITEM_PADDING")

        self.grid_columnconfigure(index=1, weight=1)
        self.grid_columnconfigure(index=2, weight=1)

        self.grid_rowconfigure(index=0, weight=1)

        self.interval_label = VariableLabel(self, language_handler=language_handler, label_key="CLICK_INTERVAL_LABEL")
        self.interval_label.grid(row=0, column=0, padx=item_padding, pady=item_padding, sticky="ew")

        self.interval_entry = IntegerEntry(self, variable_name="CLICK_INTERVAL", max_length=master.getvar(name="MAX_CLICK_INTERVAL_DIGITS"),
                                           min_value=master.getvar(name="MIN_CLICK_INTERVAL"))
        self.interval_entry.grid(row=0, column=1, padx=item_padding, pady=item_padding, sticky="ew")

        self.interval_timescale_dropdown = VariableDropdown(self, language_handler=language_handler, label_keys=["MILLISECONDS_CHOICE", "SECONDS_CHOICE", "MINUTES_CHOICE", "HOURS_CHOICE"], command=self.interval_timescale_callback)
        self.interval_timescale_dropdown.configure(variable=tkinter.StringVar(value=language_handler.scales[master.getvar(name="CLICK_INTERVAL_SCALE")]))
        self.interval_timescale_dropdown.grid(row=0, column=2, padx=item_padding, pady=item_padding, sticky="ew")

    def interval_timescale_callback(self, option_value: str) -> None:
        self.master.setvar(name="CLICK_INTERVAL_SCALE", value=self.language_handler.scales[option_value])
