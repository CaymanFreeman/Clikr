import logging
import multiprocessing
import sys

import customtkinter

from gui.frames.appearance_frame import AppearanceFrame
from gui.frames.click_interval_frame import ClickIntervalFrame
from gui.frames.click_length_frame import ClickLengthFrame
from gui.frames.click_style_frame import ClickStyleFrame
from gui.frames.hotkey_frame import HotkeyFrame
from gui.frames.language_frame import LanguageFrame
from gui.frames.location_frame import LocationFrame
from gui.frames.start_stop_frame import StartStopFrame
from handlers.appearance_handler import AppearanceHandler
from handlers.config_handler import ConfigHandler, THEME_PATH, ICON_PATH
from handlers.language_handler import LanguageHandler
from handlers.log_handler import LogHandler


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        ConfigHandler.read_config(self)
        language_handler = LanguageHandler(self)
        self.protocol(
            name="WM_DELETE_WINDOW",
            func=lambda: ConfigHandler.save_config_and_exit(self),
        )

        appearance_variables = AppearanceHandler()

        customtkinter.set_appearance_mode(self.getvar(name="APPEARANCE_MODE"))
        customtkinter.set_default_color_theme(THEME_PATH)

        self.title(language_handler.labels["TITLE"])
        self.iconbitmap(ICON_PATH)
        self.resizable(
            width=self.getvar(name="RESIZABLE_WIDTH"),
            height=self.getvar(name="RESIZABLE_HEIGHT"),
        )

        frame_padding = self.getvar(name="FRAME_PADDING")

        logging.info("Adding appearance frame...")
        appearance_frame = AppearanceFrame(
            master=self, language_handler=language_handler
        )
        appearance_frame.grid(
            row=0, column=0, padx=frame_padding, pady=frame_padding, sticky="ew"
        )
        logging.info("Added appearance frame")

        logging.info("Adding language frame...")
        language_frame = LanguageFrame(master=self, language_handler=language_handler)
        language_frame.grid(
            row=1, column=0, padx=frame_padding, pady=frame_padding, sticky="ew"
        )
        logging.info("Added language frame")

        logging.info("Adding click length frame...")
        click_length_frame = ClickLengthFrame(
            master=self, language_handler=language_handler
        )
        click_length_frame.grid(
            row=2, column=0, padx=frame_padding, pady=frame_padding, sticky="ew"
        )
        logging.info("Added click length frame")

        logging.info("Adding interval frame...")
        interval_frame = ClickIntervalFrame(
            master=self, language_handler=language_handler
        )
        interval_frame.grid(
            row=3, column=0, padx=frame_padding, pady=frame_padding, sticky="ew"
        )
        logging.info("Added interval frame")

        logging.info("Adding click style frame...")
        click_style_frame = ClickStyleFrame(
            master=self, language_handler=language_handler
        )
        click_style_frame.grid(
            row=4, column=0, padx=frame_padding, pady=frame_padding, sticky="ew"
        )
        logging.info("Added click style frame")

        logging.info("Adding location frame...")
        location_frame = LocationFrame(
            master=self,
            appearance_handler=appearance_variables,
            language_handler=language_handler,
        )
        location_frame.grid(
            row=5, column=0, padx=frame_padding, pady=frame_padding, sticky="ew"
        )
        logging.info("Added location frame")

        logging.info("Adding start-stop frame...")
        start_stop_frame = StartStopFrame(
            master=self,
            appearance_handler=appearance_variables,
            language_handler=language_handler,
        )
        start_stop_frame.grid(
            row=7, column=0, padx=frame_padding, pady=frame_padding, sticky="ew"
        )
        logging.info("Added start-stop frame")

        logging.info("Adding hotkey frame...")
        hotkey_frame = HotkeyFrame(
            master=self,
            start_stop_frame=start_stop_frame,
            appearance_handler=appearance_variables,
            language_handler=language_handler,
        )
        hotkey_frame.grid(
            row=6, column=0, padx=frame_padding, pady=frame_padding, sticky="ew"
        )
        logging.info("Added hotkey frame")

        logging.info("Updating window...")
        self.update()


def main():
    LogHandler.setup_logging()
    if sys.platform.startswith("win"):
        multiprocessing.freeze_support()
    logging.info("Creating app...")
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()