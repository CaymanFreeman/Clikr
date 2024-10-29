import tkinter

import customtkinter

from integer_entry import IntegerEntry
from label_variables import LabelVariables, translate_mouse_button, detranslate_mouse_button


class ClickStyleFrame(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTk, label_variables: LabelVariables):
        super().__init__(master)
        self.label_variables = label_variables
        
        item_padding = master.getvar(name="ITEM_PADDING")

        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.mouse_button_label = customtkinter.CTkLabel(self, text=label_variables.MOUSE_BUTTON_LABEL)
        self.mouse_button_label.grid(row=0, column=0, padx=item_padding, pady=item_padding, sticky="ew")

        self.mouse_button_dropdown = customtkinter.CTkOptionMenu(self, values=[label_variables.MOUSE_1_CHOICE, label_variables.MOUSE_2_CHOICE,
                                                                               label_variables.MOUSE_3_CHOICE],
                                                                 command=self.mouse_button_callback)
        self.mouse_button_dropdown.grid(row=0, column=1, padx=item_padding, pady=item_padding, sticky="ew")
        self.mouse_button_dropdown.configure(variable=tkinter.StringVar(value=translate_mouse_button(label_variables=label_variables, button=master.getvar(name="MOUSE_BUTTON"))))

        self.clicks_per_event_label = customtkinter.CTkLabel(self, text=label_variables.CLICKS_PER_EVENT_LABEL)
        self.clicks_per_event_label.grid(row=1, column=0, padx=item_padding, pady=item_padding, sticky="ew")

        self.clicks_per_event_entry = IntegerEntry(self, variable_name="CLICKS_PER_EVENT",
                                                   max_length=master.getvar(name="MAX_CLICKS_PER_EVENT_DIGITS"))
        self.clicks_per_event_entry.grid(row=1, column=1, padx=item_padding, pady=item_padding, sticky="ew")

        self.click_events_label = customtkinter.CTkLabel(self, text=label_variables.CLICK_EVENTS_LABEL)
        self.click_events_label.grid(row=2, column=0, padx=item_padding, pady=item_padding, sticky="ew")

        self.click_events_entry = IntegerEntry(self, variable_name="CLICK_EVENTS", min_value=0, max_length=master.getvar(name="MAX_CLICK_EVENTS_DIGITS"))
        self.click_events_entry.grid(row=2, column=1, padx=item_padding, pady=item_padding, sticky="ew")

    def mouse_button_callback(self, option_value: str) -> None:
        self.master.setvar(name="MOUSE_BUTTON", value=detranslate_mouse_button(label_variables=self.label_variables, button=option_value))
