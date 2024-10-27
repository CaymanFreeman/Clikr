import customtkinter
import keyboard

from start_stop_frame import StartStopFrame
from constants import *


class HotkeyFrame(customtkinter.CTkFrame):
    def __init__(self, master, start_stop_frame: StartStopFrame):
        super().__init__(master)
        self.start_stop_frame = start_stop_frame

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(0, weight=1)

        self.hotkey_value = DEFAULT_HOTKEY

        self.hotkey_label = customtkinter.CTkLabel(self, text=HOTKEY_LABEL)
        self.hotkey_label.grid(row=0, column=0, padx=ITEM_PADDING, pady=ITEM_PADDING, sticky="ew")

        self.hotkey_textbox = customtkinter.CTkTextbox(self, activate_scrollbars=False)
        self.hotkey_textbox.insert("0.0", self.hotkey_value.upper())
        self.hotkey_textbox.configure(state="disabled", width=50, height=20)
        keyboard.add_hotkey(self.hotkey_value, lambda: self.start_stop_frame.hotkey_toggle())
        self.hotkey_textbox.grid(row=0, column=1, padx=ITEM_PADDING, pady=ITEM_PADDING, sticky="ew")

        self.change_hotkey_button = customtkinter.CTkButton(self, text=CHANGE_HOTKEY_LABEL, command=self.change_hotkey_callback)
        self.change_hotkey_button.grid(row=0, column=2, padx=ITEM_PADDING, pady=ITEM_PADDING, sticky="ew")
        self.recording_hotkey = False
        self.pressed_keys = []

    def change_hotkey_callback(self) -> None:
        self.start_stop_frame.terminate_click_process()
        if self.recording_hotkey:
            keyboard.unhook_all()
            if self.pressed_keys:
                keyboard.clear_all_hotkeys()
                self.hotkey_value = "+".join(self.pressed_keys)
                keyboard.add_hotkey(self.hotkey_value, lambda: self.start_stop_frame.hotkey_toggle())
            self.change_hotkey_button.configure(text=CHANGE_HOTKEY_LABEL, fg_color=BUTTON_BLUE_FG, hover_color=BUTTON_BLUE_HOVER)
            self.hotkey_textbox.configure(text_color=GRAY)
            self.change_hotkey_text(self.hotkey_value.upper())
            self.pressed_keys.clear()
            self.start_stop_frame.prevent_click_processes = False
        else:
            self.start_stop_frame.prevent_click_processes = True
            self.change_hotkey_button.configure(text=CONFIRM_HOTKEY_LABEL, fg_color=HOTKEY_BUTTON_GREEN_FG, hover_color=HOTKEY_BUTTON_GREEN_HOVER)
            self.hotkey_textbox.configure(text_color=HOTKEY_BUTTON_GREEN_FG)
            self.change_hotkey_text(HOTKEY_ENTRY_RECORDING)
            self.pressed_keys.clear()
            keyboard.hook(self.on_key_event)
        self.recording_hotkey = not self.recording_hotkey

    def on_key_event(self, event) -> None:
        if not self.recording_hotkey:
            return

        if event.event_type == keyboard.KEY_DOWN:
            key_name = event.name.lower()
            if key_name in ['left shift', 'right shift']:
                key_name = 'shift'
            elif key_name in ['left ctrl', 'right ctrl']:
                key_name = 'ctrl'
            elif key_name in ['left alt', 'right alt']:
                key_name = 'alt'

            if len(self.pressed_keys) < 3 and key_name not in self.pressed_keys:
                self.pressed_keys.append(key_name)
                current_keys = "+".join(self.pressed_keys)
                self.change_hotkey_text(current_keys.upper())

    def change_hotkey_text(self, new_text) -> None:
        self.hotkey_textbox.configure(state="normal")
        self.hotkey_textbox.delete("0.0", "end")
        self.hotkey_textbox.insert("0.0", new_text)
        self.hotkey_textbox.configure(state="disabled")
