import customtkinter

from handlers.language_handler import LanguageHandler


class VariableLabel(customtkinter.CTkLabel):
    def __init__(self, master, language_handler: LanguageHandler, label_key: str, **kwargs):
        super().__init__(master, text=language_handler.labels[label_key], **kwargs)
        self.language_handler = language_handler
        self.label_key = label_key
        language_handler.labeled_item_registry.append(self)

    def reload(self):
        self.configure(text=self.language_handler.labels[self.label_key])
