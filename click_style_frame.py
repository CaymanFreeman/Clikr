import tkinter

import customtkinter

from integer_entry import IntegerEntry
from language_handler import LanguageHandler
from variable_dropdown import VariableDropdown
from variable_label import VariableLabel


class ClickStyleFrame(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTk, language_handler: LanguageHandler):
        super().__init__(master)
        self.language_handler = language_handler
        
        item_padding = master.getvar(name="ITEM_PADDING")

        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.mouse_button_label = VariableLabel(self, language_handler=language_handler, label_key="MOUSE_BUTTON_LABEL")
        self.mouse_button_label.grid(row=0, column=0, padx=item_padding, pady=item_padding, sticky="ew")

        self.mouse_button_dropdown = VariableDropdown(self, language_handler=language_handler, label_keys=["MOUSE_1_CHOICE", "MOUSE_2_CHOICE", "MOUSE_3_CHOICE"], command=self.mouse_button_dropdown_callback)
        self.mouse_button_dropdown.grid(row=0, column=1, padx=item_padding, pady=item_padding, sticky="ew")
        self.mouse_button_dropdown.configure(variable=tkinter.StringVar(value=language_handler.mouse_buttons[master.getvar(name="MOUSE_BUTTON")]))

        self.clicks_per_event_label = VariableLabel(self, language_handler=language_handler, label_key="CLICKS_PER_EVENT_LABEL")
        self.clicks_per_event_label.grid(row=1, column=0, padx=item_padding, pady=item_padding, sticky="ew")

        self.clicks_per_event_entry = IntegerEntry(self, variable_name="CLICKS_PER_EVENT",
                                                   max_length=master.getvar(name="MAX_CLICKS_PER_EVENT_DIGITS"))
        self.clicks_per_event_entry.grid(row=1, column=1, padx=item_padding, pady=item_padding, sticky="ew")

        self.click_events_label = VariableLabel(self, language_handler=language_handler, label_key="CLICK_EVENTS_LABEL")
        self.click_events_label.grid(row=2, column=0, padx=item_padding, pady=item_padding, sticky="ew")

        self.click_events_entry = IntegerEntry(self, variable_name="CLICK_EVENTS", min_value=0, max_length=master.getvar(name="MAX_CLICK_EVENTS_DIGITS"))
        self.click_events_entry.grid(row=2, column=1, padx=item_padding, pady=item_padding, sticky="ew")

    def mouse_button_dropdown_callback(self, option_value: str) -> None:
        self.master.setvar(name="MOUSE_BUTTON", value=self.language_handler.mouse_buttons[option_value])
