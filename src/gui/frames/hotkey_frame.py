import customtkinter
import keyboard

from gui.frames.start_stop_frame import StartStopFrame
from gui.items.variable_button import VariableButton
from gui.items.variable_label import VariableLabel
from handlers.appearance_handler import AppearanceHandler
from handlers.language_handler import LanguageHandler


class HotkeyFrame(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTk, start_stop_frame: StartStopFrame,
                 appearance_handler: AppearanceHandler, language_handler: LanguageHandler):
        super().__init__(master)
        self.start_stop_frame = start_stop_frame
        self.appearance_variables = appearance_handler
        self.language_handler = language_handler

        item_padding = master.getvar(name="ITEM_PADDING")

        self.grid_columnconfigure(index=1, weight=1)
        self.grid_columnconfigure(index=2, weight=1)

        self.grid_rowconfigure(index=0, weight=1)

        self.hotkey_value = master.getvar(name="HOTKEY")

        self.hotkey_label = VariableLabel(self, language_handler=language_handler, label_key="HOTKEY_LABEL")
        self.hotkey_label.grid(row=0, column=0, padx=item_padding, pady=item_padding, sticky="ew")

        self.hotkey_textbox = customtkinter.CTkTextbox(self, activate_scrollbars=False)
        self.hotkey_textbox.insert(index="0.0", text=self.hotkey_value.upper())
        self.hotkey_textbox.configure(state="disabled", width=50, height=20)
        keyboard.add_hotkey(self.hotkey_value, lambda: self.start_stop_frame.hotkey_toggle())
        self.hotkey_textbox.grid(row=0, column=1, padx=item_padding, pady=item_padding, sticky="ew")

        self.change_hotkey_button = VariableButton(self, language_handler=language_handler,
                                                   label_key="CHANGE_HOTKEY_LABEL", command=self.change_hotkey_callback)
        self.change_hotkey_button.grid(row=0, column=2, padx=item_padding, pady=item_padding, sticky="ew")
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
                self.master.setvar(name="HOTKEY", value=self.hotkey_value)
            self.change_hotkey_button.configure(text=self.language_handler.labels["CHANGE_HOTKEY_LABEL"],
                                                fg_color=self.appearance_variables.BUTTON_FG_COLOR,
                                                hover_color=self.appearance_variables.BUTTON_HOVER_COLOR)
            self.hotkey_textbox.configure(text_color=self.appearance_variables.LABEL_TEXT_COLOR)
            self.change_hotkey_text(self.hotkey_value.upper())
            self.pressed_keys.clear()
            self.start_stop_frame.prevent_click_processes = False
        else:
            self.start_stop_frame.prevent_click_processes = True
            self.change_hotkey_button.configure(text=self.language_handler.labels["CONFIRM_HOTKEY_LABEL"],
                                                fg_color=self.appearance_variables.BUTTON_CONFIRM_FG_COLOR,
                                                hover_color=self.appearance_variables.BUTTON_CONFIRM_HOVER_COLOR)
            self.hotkey_textbox.configure(text_color=self.appearance_variables.BUTTON_CONFIRM_FG_COLOR)
            self.change_hotkey_text(self.language_handler.labels["HOTKEY_RECORDING_LABEL"])
            self.pressed_keys.clear()
            keyboard.hook(callback=self.on_key_event)
        self.recording_hotkey = not self.recording_hotkey

    def on_key_event(self, keyboard_event: keyboard.KeyboardEvent) -> None:
        if not self.recording_hotkey:
            return

        if keyboard_event.event_type == keyboard.KEY_DOWN:
            key_name = keyboard_event.name.lower()
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

    def change_hotkey_text(self, new_text: str) -> None:
        self.hotkey_textbox.configure(state="normal")
        self.hotkey_textbox.delete(index1="0.0", index2="end")
        self.hotkey_textbox.insert(index="0.0", text=new_text)
        self.hotkey_textbox.configure(state="disabled")
