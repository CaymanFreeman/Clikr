import multiprocessing

import customtkinter

from click_process import ClickProcess
from constants import *

class StartStopFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.click_process = None
        self.prevent_click_processes = False
        self.terminated_event = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=1)

        self.start_button = customtkinter.CTkButton(self, text=START_BUTTON_LABEL, command=self.start_button_callback, height=50)
        self.start_button.grid(row=0, column=0, padx=ITEM_PADDING, pady=ITEM_PADDING, sticky="ew")

        self.stop_button = customtkinter.CTkButton(self, text=STOP_BUTTON_LABEL, command=self.stop_button_callback, height=50)
        self.stop_button.configure(state="disabled", fg_color=DARK_GRAY)
        self.stop_button.grid(row=0, column=1, padx=ITEM_PADDING, pady=ITEM_PADDING, sticky="ew")

        self.after(10, self.monitor_click_process)

    def toggle_start_stop_buttons(self):
        if self.start_button.cget("state") == "normal":
            self.start_button.configure(state="disabled", fg_color=DARK_GRAY)
            self.stop_button.configure(state="normal", fg_color=BUTTON_BLUE_FG)
        else:
            self.start_button.configure(state="normal", fg_color=BUTTON_BLUE_FG)
            self.stop_button.configure(state="disabled", fg_color=DARK_GRAY)

    def stop_button_callback(self):
        self.terminated_event.set()

    def start_button_callback(self) -> None:
        if self.prevent_click_processes:
            return
        self.terminated_event = multiprocessing.Event()
        self.click_process = ClickProcess(
            self.master.getvar("CLICK_INTERVAL"),
            self.master.getvar("INTERVAL_TIMESCALE"),
            self.master.getvar("CLICK_LENGTH"),
            self.master.getvar("LENGTH_TIMESCALE"),
            self.master.getvar("MOUSE_BUTTON"),
            self.master.getvar("CLICKS_PER_EVENT"),
            self.master.getvar("CLICK_EVENTS"),
            self.master.getvar("CLICK_LOCATION"),
            self.terminated_event
        )
        self.click_process.start()
        self.toggle_start_stop_buttons()

    def monitor_click_process(self) -> None:
        if self.terminated_event and self.terminated_event.is_set():
            self.terminate_click_process()
        self.after(10, self.monitor_click_process)

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

