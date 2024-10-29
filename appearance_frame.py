import customtkinter

from config_handler import CHANGE_APPEARANCE_LABEL


class AppearanceFrame(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTk):
        super().__init__(master)

        item_padding = master.getvar(name="ITEM_PADDING")

        self.grid_columnconfigure(index=0, weight=1)

        self.appearance_button = customtkinter.CTkButton(self, text=CHANGE_APPEARANCE_LABEL,
                                                         command=self.appearance_button_callback)
        self.appearance_button.grid(row=0, column=0, padx=item_padding, pady=item_padding, sticky="ew")

    @staticmethod
    def appearance_button_callback() -> None:
        if customtkinter.get_appearance_mode() == "Dark":
            customtkinter.set_appearance_mode("Light")
        else:
            customtkinter.set_appearance_mode("Dark")
