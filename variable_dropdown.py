import tkinter

import customtkinter

from language_handler import LanguageHandler


class VariableDropdown(customtkinter.CTkOptionMenu):
    def __init__(self, master, language_handler: LanguageHandler, label_keys: list[str], **kwargs):
        values = []
        for label_key in label_keys:
            values.append(language_handler.labels[label_key])
        super().__init__(master, values=values, **kwargs)
        self.language_handler = language_handler
        self.label_keys = label_keys
        language_handler.labeled_item_registry.append(self)

    def reload(self):
        values = []
        for label_key in self.label_keys:
            values.append(self.language_handler.labels[label_key])
        self.configure(values=values)
        self.configure(variable=tkinter.StringVar(value=self.language_handler.mouse_buttons[self.master.getvar(name="MOUSE_BUTTON")]))