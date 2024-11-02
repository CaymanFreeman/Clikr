import threading
import time

import customtkinter
import keyboard
import mouse
from gui.items.variable_button import VariableButton
from gui.items.variable_label import VariableLabel
from handlers.appearance_handler import AppearanceHandler
from handlers.language_handler import LanguageHandler


class LocationFrame(customtkinter.CTkFrame):
    def __init__(
        self,
        master: customtkinter.CTk,
        appearance_handler: AppearanceHandler,
        language_handler: LanguageHandler,
    ):
        super().__init__(master)
        self.appearance_variables = appearance_handler
        self.label_variables = language_handler

        self.cancel_pick_handler = None
        self.pick_handler = None
        self.click_location = master.getvar(name="CLICK_LOCATION")
        self.location_locked = self.click_location != "none"

        item_padding = master.getvar(name="ITEM_PADDING")

        self.grid_columnconfigure(index=1, weight=1)
        self.grid_columnconfigure(index=2, weight=1)

        self.grid_rowconfigure(index=0, weight=1)

        self.location_label = VariableLabel(
            self, language_handler=language_handler, label_key="LOCATION_LABEL"
        )
        self.location_label.grid(
            row=0, column=0, padx=item_padding, pady=item_padding, sticky="ew"
        )

        self.location_textbox = customtkinter.CTkTextbox(
            self, activate_scrollbars=False
        )
        self.location_textbox.insert(index="0.0", text=str(self.click_location))
        self.location_textbox.configure(state="disabled", width=50, height=20)
        self.location_textbox.grid(
            row=0, column=1, padx=item_padding, pady=item_padding, sticky="ew"
        )

        self.pick_location_button = VariableButton(
            self,
            language_handler=language_handler,
            label_key="PICK_LOCATION_LABEL",
            command=self.pick_location_callback,
        )
        self.pick_location_button.grid(
            row=0, column=2, padx=item_padding, pady=item_padding, sticky="ew"
        )

        if self.location_locked:
            self.location_textbox.configure(
                text_color=self.appearance_variables.label_text_disabled_color
            )

        threading.Thread(target=self.location_update_process, daemon=True).start()

    def pick_location_callback(self) -> None:
        self.location_locked = False
        threading.Thread(target=self.location_update_process, daemon=True).start()
        self.pick_location_button.configure(
            text=self.label_variables.labels["LOCATION_CONFIRM_LABEL"],
            fg_color=self.appearance_variables.button_disabled_color,
            state="disabled",
        )
        self.location_textbox.configure(
            text_color=self.appearance_variables.label_text_color
        )
        time.sleep(0.1)
        self.pick_handler = mouse.on_click(callback=self.pick_location)
        self.cancel_pick_handler = keyboard.on_press_key(
            key=self.master.getvar(name="CANCEL_LOCATION_PICK_KEY"),
            callback=self.cancel_pick_location,
        )

    def unhook_pick_keys(self):
        if self.cancel_pick_handler:
            keyboard.unhook(remove=self.cancel_pick_handler)
        if self.pick_handler:
            mouse.unhook(callback=self.pick_handler)

    def cancel_pick_location(self, _keyboard_event: keyboard.KeyboardEvent):
        self.unhook_pick_keys()
        self.master.setvar(name="CLICK_LOCATION", value="none")
        threading.Thread(target=self.location_update_process, daemon=True).start()
        self.location_textbox.configure(
            text_color=self.appearance_variables.label_text_color
        )
        self.pick_location_button.configure(
            text=self.label_variables.labels["PICK_LOCATION_LABEL"],
            fg_color=self.appearance_variables.button_fg_color,
            state="normal",
        )

    def pick_location(self):
        self.unhook_pick_keys()
        location = tuple(mouse.get_position())
        self.master.setvar(name="CLICK_LOCATION", value=str(location))
        self.click_location = location
        self.update_location(location)
        self.location_locked = True
        self.location_textbox.configure(
            text_color=self.appearance_variables.label_text_disabled_color
        )
        self.pick_location_button.configure(
            text=self.label_variables.labels["PICK_LOCATION_LABEL"],
            fg_color=self.appearance_variables.button_fg_color,
            state="normal",
        )

    def update_location(self, location) -> None:
        self.click_location = location
        self.location_textbox.configure(state="normal")
        self.location_textbox.delete(index1="0.0", index2="end")
        self.location_textbox.insert(index="0.0", text=str(self.click_location))
        self.location_textbox.configure(state="disabled")

    def location_update_process(self) -> None:
        update_interval = float(
            self.master.getvar(name="LOCATION_UPDATE_INTERVAL_SECONDS")
        )
        while True:
            if not self.location_locked:
                time.sleep(update_interval)
                try:
                    cursor_location = tuple(mouse.get_position())
                    if self.click_location != cursor_location:
                        self.update_location(cursor_location)
                except Exception as e:
                    print(f"Location process error: {e}")
            else:
                break
