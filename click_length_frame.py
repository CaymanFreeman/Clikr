import customtkinter

from constants import *
from integer_entry import IntegerEntry


class ClickLengthFrame(customtkinter.CTkFrame):

    def __init__(self, master: customtkinter.CTk):
        super().__init__(master)

        self.grid_columnconfigure(index=1, weight=1)
        self.grid_columnconfigure(index=2, weight=1)

        self.grid_rowconfigure(index=0, weight=1)

        self.length_label = customtkinter.CTkLabel(self, text=CLICK_LENGTH_LABEL)
        self.length_label.grid(row=0, column=0, padx=ITEM_PADDING, pady=ITEM_PADDING, sticky="ew")

        self.length_entry = IntegerEntry(self, variable_name="CLICK_LENGTH", default_value=DEFAULT_LENGTH,
                                         max_length=MAX_CLICK_INTERVAL_DIGITS, min_value=MIN_CLICK_INTERVAL)
        self.length_entry.grid(row=0, column=1, padx=ITEM_PADDING, pady=ITEM_PADDING, sticky="ew")

        self.length_timescale_dropdown = (customtkinter.CTkOptionMenu(self, values=[MILLISECONDS_CHOICE, SECONDS_CHOICE,
                                                                                    MINUTES_CHOICE, HOURS_CHOICE],
                                                                      command=self.length_timescale_callback))
        self.length_timescale_dropdown.grid(row=0, column=2, padx=ITEM_PADDING, pady=ITEM_PADDING, sticky="ew")
        self.master.setvar(name="LENGTH_TIMESCALE", value=MILLISECONDS_CHOICE)

    def length_timescale_callback(self, option_value) -> None:
        self.master.setvar(name="LENGTH_TIMESCALE", value=option_value)
