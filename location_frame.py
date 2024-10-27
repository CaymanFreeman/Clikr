import threading
import time

import customtkinter
import mouse

from constants import *


class LocationFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.cursor_location = (0, 0)
        self.master.setvar("CLICK_LOCATION", "none")
        self.location_locked = False

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(0, weight=1)

        self.hotkey_value = DEFAULT_HOTKEY

        self.location_label = customtkinter.CTkLabel(self, text=LOCATION_LABEL)
        self.location_label.grid(row=0, column=0, padx=ITEM_PADDING, pady=ITEM_PADDING, sticky="ew")

        self.location_textbox = customtkinter.CTkTextbox(self, activate_scrollbars=False)
        self.location_textbox.insert("0.0", self.location_string)
        self.location_textbox.configure(state="disabled", width=50, height=20)
        self.location_textbox.grid(row=0, column=1, padx=ITEM_PADDING, pady=ITEM_PADDING, sticky="ew")

        self.pick_location_button = customtkinter.CTkButton(self, text=PICK_LOCATION_LABEL,
                                                            command=self.pick_location_callback)
        self.pick_location_button.grid(row=0, column=2, padx=ITEM_PADDING, pady=ITEM_PADDING, sticky="ew")

        threading.Thread(target=self.location_update_process, daemon=True).start()

    def pick_location_callback(self) -> None:
        self.location_locked = False
        threading.Thread(target=self.location_update_process, daemon=True).start()
        self.pick_location_button.configure(text=LOCATION_CONFIRM_LABEL, fg_color=DARK_GRAY, state="disabled")
        self.location_textbox.configure(state="normal", text_color=GRAY)
        time.sleep(0.1)
        mouse.on_click(self.pick_location)

    def pick_location(self):
        location = tuple(mouse.get_position())
        mouse.unhook_all()
        self.master.setvar("CLICK_LOCATION", str(location))
        self.cursor_location = location
        self.update_location(location)
        self.location_locked = True
        self.location_textbox.configure(state="disabled", text_color=DARK_GRAY)
        self.pick_location_button.configure(text=PICK_LOCATION_LABEL, fg_color=BUTTON_BLUE_FG, state="normal")

    def update_location(self, location) -> None:
        self.cursor_location = location
        self.location_textbox.configure(state="normal")
        self.location_textbox.delete("0.0", "end")
        self.location_textbox.insert("0.0", self.location_string)
        self.location_textbox.configure(state="disabled")

    @property
    def location_string(self) -> str:
        return str(self.cursor_location)

    def location_update_process(self) -> None:
        while True:
            if not self.location_locked:
                time.sleep(LOCATION_UPDATE_INTERVAL)
                try:
                    cursor_location = tuple(mouse.get_position())
                    if self.cursor_location != cursor_location:
                        self.update_location(cursor_location)
                except Exception as e:
                    print(f"Location process error: {e}")
            else:
                break
