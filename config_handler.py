from configparser import ConfigParser
from os.path import isfile

import customtkinter

CONFIG_PATH = "config.ini"

LABEL_TEXT_COLOR = ("#2A2A2A", "#e8edfc")
LABEL_TEXT_DISABLED_COLOR = ("#545454", "#BABFC7")
BUTTON_TEXT_COLOR = "#ffffff"
BUTTON_DISABLED_COLOR = ("#979DA2", "#565B5E")
BUTTON_FG_COLOR = "#428dff"
BUTTON_GREEN_FG_COLOR = "#469546"
BUTTON_HOVER_COLOR = "#3670cc"
BUTTON_GREEN_HOVER_COLOR = "#326A32"

MILLISECONDS_CHOICE = "Milliseconds"
SECONDS_CHOICE = "Seconds"
MINUTES_CHOICE = "Minutes"
HOURS_CHOICE = "Hours"
MOUSE_1_CHOICE = "Left (M1)"
MOUSE_2_CHOICE = "Right (M2)"
MOUSE_3_CHOICE = "Middle (M3)"

CHANGE_APPEARANCE_LABEL = "Change Appearance"
CHANGE_HOTKEY_LABEL = "Change Hotkey"
CLICK_EVENTS_LABEL = "Click Events"
CLICK_INTERVAL_LABEL = "Click Interval"
CLICK_LENGTH_LABEL = "Click Length"
CLICKS_PER_EVENT_LABEL = "Clicks Per Event"
CONFIRM_HOTKEY_LABEL = "Click to Confirm"
HOTKEY_RECORDING_LABEL = "Press Key(s)"
HOTKEY_LABEL = "Hotkey"
LOCATION_CONFIRM_LABEL = "Click Screen Location"
LOCATION_LABEL = "Location"
MOUSE_BUTTON_LABEL = "Mouse Button"
PICK_LOCATION_LABEL = "Pick Location"
START_BUTTON_LABEL = "Start"
STOP_BUTTON_LABEL = "Stop"

class ConfigHandler:

    @staticmethod
    def save_config_and_exit(app: customtkinter.CTk) -> None:
        config = ConfigParser()

        config["APPEARANCE"] = {}
        config["HOTKEY"] = {}
        config["CLICK_PROCESS"] = {}
        config["LOCATION"] = {}
        config["INPUT_VALIDATION"] = {}

        config["APPEARANCE"]["APPEARANCE_MODE"] = customtkinter.get_appearance_mode()
        config["APPEARANCE"]["FRAME_PADDING"] = app.getvar(name="FRAME_PADDING")
        config["APPEARANCE"]["ITEM_PADDING"] = app.getvar(name="ITEM_PADDING")
        config["APPEARANCE"]["RESIZABLE_WIDTH"] = app.getvar(name="RESIZABLE_WIDTH")
        config["APPEARANCE"]["RESIZABLE_HEIGHT"] = app.getvar(name="RESIZABLE_HEIGHT")

        config["HOTKEY"]["HOTKEY"] = app.getvar(name="HOTKEY")

        config["CLICK_PROCESS"]["CLICK_EVENTS"] = app.getvar(name="CLICK_EVENTS")
        config["CLICK_PROCESS"]["CLICKS_PER_EVENT"] = app.getvar(name="CLICKS_PER_EVENT")
        config["CLICK_PROCESS"]["CLICK_INTERVAL"] = app.getvar(name="CLICK_INTERVAL")
        config["CLICK_PROCESS"]["CLICK_INTERVAL_SCALE"] = app.getvar(name="CLICK_INTERVAL_SCALE")
        config["CLICK_PROCESS"]["CLICK_LENGTH"] = app.getvar(name="CLICK_LENGTH")
        config["CLICK_PROCESS"]["CLICK_LENGTH_SCALE"] = app.getvar(name="CLICK_LENGTH_SCALE")
        config["CLICK_PROCESS"]["MOUSE_BUTTON"] = app.getvar(name="MOUSE_BUTTON")
        config["CLICK_PROCESS"]["CLICK_LOCATION"] = app.getvar(name="CLICK_LOCATION")

        config["LOCATION"]["CANCEL_LOCATION_PICK_KEY"] = app.getvar(name="CANCEL_LOCATION_PICK_KEY")
        config["LOCATION"]["LOCATION_UPDATE_INTERVAL_SECONDS"] = app.getvar(name="LOCATION_UPDATE_INTERVAL_SECONDS")

        config["INPUT_VALIDATION"]["MAX_HOTKEY_KEYS"] = app.getvar(name="MAX_HOTKEY_KEYS")
        config["INPUT_VALIDATION"]["MAX_CLICK_EVENTS_DIGITS"] = app.getvar(name="MAX_CLICK_EVENTS_DIGITS")
        config["INPUT_VALIDATION"]["MAX_CLICKS_PER_EVENT_DIGITS"] = app.getvar(name="MAX_CLICKS_PER_EVENT_DIGITS")
        config["INPUT_VALIDATION"]["MAX_CLICK_INTERVAL_DIGITS"] = app.getvar(name="MAX_CLICK_INTERVAL_DIGITS")
        config["INPUT_VALIDATION"]["MIN_CLICK_INTERVAL"] = app.getvar(name="MIN_CLICK_INTERVAL")

        with open(CONFIG_PATH, "w") as file:
            config.write(file)
        app.destroy()

    @staticmethod
    def initialize_config(app: customtkinter.CTk) -> None:
        ConfigHandler.create_defaults()
        ConfigHandler.read_config(app)

    @staticmethod
    def read_config(app: customtkinter.CTk) -> None:
        config = ConfigParser()
        config.read(CONFIG_PATH)
        try:
            for section in config.sections():
                for name, value in config.items(section):
                    app.setvar(name.upper(), value)
        except Exception as error:
            print(f"Error loading config: {error}")
            exit(0)

    @staticmethod
    def create_defaults() -> None:
        if isfile(CONFIG_PATH):
            return
        default_config = ConfigParser()

        default_config["APPEARANCE"] = {
            "APPEARANCE_MODE": "Dark",
            "FRAME_PADDING": "3",
            "ITEM_PADDING": "5",
            "RESIZABLE_WIDTH": "False",
            "RESIZABLE_HEIGHT": "False"
        }

        default_config["HOTKEY"] = {
            "HOTKEY": "ctrl+f8"
        }

        default_config["CLICK_PROCESS"] = {
            "CLICK_EVENTS": "0",
            "CLICKS_PER_EVENT": "1",
            "CLICK_INTERVAL": "100",
            "CLICK_INTERVAL_SCALE": MILLISECONDS_CHOICE,
            "CLICK_LENGTH": "0",
            "CLICK_LENGTH_SCALE": MILLISECONDS_CHOICE,
            "MOUSE_BUTTON": MOUSE_1_CHOICE,
            "CLICK_LOCATION": "none"
        }

        default_config["LOCATION"] = {
            "CANCEL_LOCATION_PICK_KEY": "escape",
            "LOCATION_UPDATE_INTERVAL_SECONDS": "0.05"
        }

        default_config["INPUT_VALIDATION"] = {
            "MAX_HOTKEY_KEYS": "3",
            "MAX_CLICK_EVENTS_DIGITS": "6",
            "MAX_CLICKS_PER_EVENT_DIGITS": "3",
            "MAX_CLICK_INTERVAL_DIGITS": "6",
            "MIN_CLICK_INTERVAL": "0"
        }

        with open(CONFIG_PATH, "w") as file:
            default_config.write(file)