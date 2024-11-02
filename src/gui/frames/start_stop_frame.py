import multiprocessing

import customtkinter
from gui.items.variable_button import VariableButton
from handlers.appearance_handler import AppearanceHandler
from handlers.click_handler import ClickHandler
from handlers.language_handler import LanguageHandler


class StartStopFrame(customtkinter.CTkFrame):
    def __init__(
        self,
        master: customtkinter.CTk,
        appearance_handler: AppearanceHandler,
        language_handler: LanguageHandler,
    ):
        super().__init__(master)
        self.appearance_variables = appearance_handler

        self.click_process = None
        self.prevent_click_processes = False
        self.terminated_event = None

        item_padding = master.getvar(name="ITEM_PADDING")

        self.grid_columnconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=1, weight=1)

        self.grid_rowconfigure(index=0, weight=1)

        self.start_button = VariableButton(
            self,
            language_handler=language_handler,
            label_key="START_BUTTON_LABEL",
            command=self.start_button_callback,
            height=50,
        )
        self.start_button.grid(
            row=0, column=0, padx=item_padding, pady=item_padding, sticky="ew"
        )

        self.stop_button = VariableButton(
            self,
            language_handler=language_handler,
            label_key="STOP_BUTTON_LABEL",
            command=self.stop_button_callback,
            height=50,
        )
        self.stop_button.configure(
            state="disabled", fg_color=self.appearance_variables.button_disabled_color
        )
        self.stop_button.grid(
            row=0, column=1, padx=item_padding, pady=item_padding, sticky="ew"
        )

        self.after(ms=10, func=self.monitor_click_process)

    def toggle_start_stop_buttons(self) -> None:
        if self.start_button.cget("state") == "normal":
            self.start_button.configure(
                state="disabled",
                fg_color=self.appearance_variables.button_disabled_color,
            )
            self.stop_button.configure(
                state="normal", fg_color=self.appearance_variables.button_fg_color
            )
        else:
            self.start_button.configure(
                state="normal", fg_color=self.appearance_variables.button_fg_color
            )
            self.stop_button.configure(
                state="disabled",
                fg_color=self.appearance_variables.button_disabled_color,
            )

    def stop_button_callback(self) -> None:
        self.terminated_event.set()

    def start_button_callback(self) -> None:
        if self.prevent_click_processes:
            return
        self.terminated_event = multiprocessing.Event()
        self.click_process = ClickHandler(
            self.master.getvar(name="CLICK_INTERVAL"),
            self.master.getvar(name="CLICK_INTERVAL_SCALE"),
            self.master.getvar(name="CLICK_LENGTH"),
            self.master.getvar(name="CLICK_LENGTH_SCALE"),
            self.master.getvar(name="MOUSE_BUTTON"),
            self.master.getvar(name="CLICKS_PER_EVENT"),
            self.master.getvar(name="CLICK_EVENTS"),
            self.master.getvar(name="CLICK_LOCATION"),
            self.terminated_event,
        )
        self.click_process.start()
        self.toggle_start_stop_buttons()

    def monitor_click_process(self) -> None:
        if self.terminated_event and self.terminated_event.is_set():
            self.terminate_click_process()
        self.after(ms=10, func=self.monitor_click_process)

    def terminate_click_process(self) -> None:
        if self.click_process and self.click_process.is_alive():
            self.click_process.terminate()
            self.click_process.join()
            self.click_process = None
            self.terminated_event = None
            self.toggle_start_stop_buttons()

    def hotkey_toggle(self) -> None:
        try:
            if self.click_process.is_alive():
                self.terminated_event.set()
            else:
                self.start_button_callback()
        except AttributeError:
            self.start_button_callback()
