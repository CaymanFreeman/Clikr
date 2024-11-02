import tkinter

import customtkinter
from gui.items.variable_label import VariableLabel
from handlers.language_handler import LanguageHandler


class LanguageFrame(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTk, language_handler: LanguageHandler):
        super().__init__(master)
        self.language_handler = language_handler

        item_padding = master.getvar(name="ITEM_PADDING")

        self.grid_columnconfigure(index=1, weight=1)

        self.language_label = VariableLabel(
            self, language_handler=language_handler, label_key="LANGUAGE_LABEL"
        )
        self.language_label.grid(
            row=0, column=0, padx=item_padding, pady=item_padding, sticky="ew"
        )

        self.language_dropdown = customtkinter.CTkOptionMenu(
            self,
            values=language_handler.language_choices,
            command=self.language_dropdown_callback,
        )
        self.language_dropdown.grid(
            row=0, column=1, padx=item_padding, pady=item_padding, sticky="ew"
        )
        self.language_dropdown.configure(
            variable=tkinter.StringVar(
                value=language_handler.languages[master.getvar(name="LANGUAGE_CODE")]
            )
        )

    def language_dropdown_callback(self, option_value: str) -> None:
        self.master.setvar(
            name="LANGUAGE_CODE", value=self.language_handler.languages[option_value]
        )
        self.language_handler.reload_labeled_items()
