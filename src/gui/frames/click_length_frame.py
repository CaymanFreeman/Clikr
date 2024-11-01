import tkinter

import customtkinter

from gui.items.integer_entry import IntegerEntry
from gui.items.variable_dropdown import VariableDropdown
from gui.items.variable_label import VariableLabel
from handlers.language_handler import LanguageHandler


class ClickLengthFrame(customtkinter.CTkFrame):

    def __init__(self, master: customtkinter.CTk, language_handler: LanguageHandler):
        super().__init__(master)
        self.language_handler = language_handler

        item_padding = master.getvar(name="ITEM_PADDING")

        self.grid_columnconfigure(index=1, weight=1)
        self.grid_columnconfigure(index=2, weight=1)

        self.grid_rowconfigure(index=0, weight=1)

        self.length_label = VariableLabel(self, language_handler=language_handler, label_key="CLICK_LENGTH_LABEL")
        self.length_label.grid(row=0, column=0, padx=item_padding, pady=item_padding, sticky="ew")

        self.length_entry = IntegerEntry(self, variable_name="CLICK_LENGTH",
                                         max_length=master.getvar(name="MAX_CLICK_INTERVAL_DIGITS"),
                                         min_value=master.getvar(name="MIN_CLICK_INTERVAL"))
        self.length_entry.grid(row=0, column=1, padx=item_padding, pady=item_padding, sticky="ew")

        self.length_timescale_dropdown = VariableDropdown(self, language_handler=language_handler,
                                                          label_keys=["MILLISECONDS_CHOICE", "SECONDS_CHOICE",
                                                                      "MINUTES_CHOICE", "HOURS_CHOICE"],
                                                          command=self.length_timescale_callback)
        self.length_timescale_dropdown.configure(
            variable=tkinter.StringVar(value=language_handler.scales[master.getvar(name="CLICK_LENGTH_SCALE")]))
        self.length_timescale_dropdown.grid(row=0, column=2, padx=item_padding, pady=item_padding, sticky="ew")

    def length_timescale_callback(self, option_value) -> None:
        self.master.setvar(name="CLICK_LENGTH_SCALE", value=self.language_handler.scales[option_value])
