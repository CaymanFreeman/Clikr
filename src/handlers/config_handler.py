import configparser
import errno
import locale
import logging
import os
import sys
from configparser import ConfigParser

import customtkinter

ROOT_PATH = os.path.abspath("")
CONFIG_PATH = os.path.join(ROOT_PATH, "config.ini")
THEME_PATH = os.path.join(ROOT_PATH, "assets", "easy_auto_clicker_theme.json")
LANGUAGES_PATH = os.path.join(ROOT_PATH, "assets", "languages")
ICON_PATH = os.path.join(ROOT_PATH, "assets", "icon.ico")


class ConfigHandler:

    default_config = {
        "LANGUAGE": {
            "LANGUAGE_CODE": "system",
            "FALLBACK_CODE": "en_us",
        },
        "APPEARANCE": {
            "APPEARANCE_MODE": "Dark",
            "FRAME_PADDING": "3",
            "ITEM_PADDING": "5",
            "RESIZABLE_WIDTH": "False",
            "RESIZABLE_HEIGHT": "False",
        },
        "HOTKEY": {"HOTKEY": "ctrl+f8"},
        "CLICK_PROCESS": {
            "CLICK_EVENTS": "0",
            "CLICKS_PER_EVENT": "1",
            "CLICK_INTERVAL": "100",
            "CLICK_INTERVAL_SCALE": "1",
            "CLICK_LENGTH": "0",
            "CLICK_LENGTH_SCALE": "1",
            "MOUSE_BUTTON": "1",
            "CLICK_LOCATION": "none",
        },
        "LOCATION": {
            "CANCEL_LOCATION_PICK_KEY": "escape",
            "LOCATION_UPDATE_INTERVAL_SECONDS": "0.05",
        },
        "INPUT_VALIDATION": {
            "MAX_HOTKEY_KEYS": "3",
            "MAX_CLICK_EVENTS_DIGITS": "6",
            "MAX_CLICKS_PER_EVENT_DIGITS": "3",
            "MAX_CLICK_INTERVAL_DIGITS": "6",
            "MIN_CLICK_INTERVAL": "0",
        },
    }

    @staticmethod
    def save_config_and_exit(app: customtkinter.CTk) -> None:
        config = ConfigParser()

        for section in ConfigHandler.default_config:
            config[section] = {}

        config["LANGUAGE"]["LANGUAGE_CODE"] = app.getvar(name="LANGUAGE_CODE")
        config["LANGUAGE"]["FALLBACK_CODE"] = app.getvar(name="FALLBACK_CODE")

        config["APPEARANCE"]["APPEARANCE_MODE"] = customtkinter.get_appearance_mode()
        config["APPEARANCE"]["FRAME_PADDING"] = app.getvar(name="FRAME_PADDING")
        config["APPEARANCE"]["ITEM_PADDING"] = app.getvar(name="ITEM_PADDING")
        config["APPEARANCE"]["RESIZABLE_WIDTH"] = app.getvar(name="RESIZABLE_WIDTH")
        config["APPEARANCE"]["RESIZABLE_HEIGHT"] = app.getvar(name="RESIZABLE_HEIGHT")

        config["HOTKEY"]["HOTKEY"] = app.getvar(name="HOTKEY")

        config["CLICK_PROCESS"]["CLICK_EVENTS"] = app.getvar(name="CLICK_EVENTS")
        config["CLICK_PROCESS"]["CLICKS_PER_EVENT"] = app.getvar(
            name="CLICKS_PER_EVENT"
        )
        config["CLICK_PROCESS"]["CLICK_INTERVAL"] = app.getvar(name="CLICK_INTERVAL")
        config["CLICK_PROCESS"]["CLICK_INTERVAL_SCALE"] = app.getvar(
            name="CLICK_INTERVAL_SCALE"
        )
        config["CLICK_PROCESS"]["CLICK_LENGTH"] = app.getvar(name="CLICK_LENGTH")
        config["CLICK_PROCESS"]["CLICK_LENGTH_SCALE"] = app.getvar(
            name="CLICK_LENGTH_SCALE"
        )
        config["CLICK_PROCESS"]["MOUSE_BUTTON"] = app.getvar(name="MOUSE_BUTTON")
        config["CLICK_PROCESS"]["CLICK_LOCATION"] = app.getvar(name="CLICK_LOCATION")

        config["LOCATION"]["CANCEL_LOCATION_PICK_KEY"] = app.getvar(
            name="CANCEL_LOCATION_PICK_KEY"
        )
        config["LOCATION"]["LOCATION_UPDATE_INTERVAL_SECONDS"] = app.getvar(
            name="LOCATION_UPDATE_INTERVAL_SECONDS"
        )

        config["INPUT_VALIDATION"]["MAX_HOTKEY_KEYS"] = app.getvar(
            name="MAX_HOTKEY_KEYS"
        )
        config["INPUT_VALIDATION"]["MAX_CLICK_EVENTS_DIGITS"] = app.getvar(
            name="MAX_CLICK_EVENTS_DIGITS"
        )
        config["INPUT_VALIDATION"]["MAX_CLICKS_PER_EVENT_DIGITS"] = app.getvar(
            name="MAX_CLICKS_PER_EVENT_DIGITS"
        )
        config["INPUT_VALIDATION"]["MAX_CLICK_INTERVAL_DIGITS"] = app.getvar(
            name="MAX_CLICK_INTERVAL_DIGITS"
        )
        config["INPUT_VALIDATION"]["MIN_CLICK_INTERVAL"] = app.getvar(
            name="MIN_CLICK_INTERVAL"
        )

        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as file:
                logging.info("Writing config options to file...")
                config.write(file)
        except PermissionError as error:
            logging.warning(
                "Permission was denied while saving config file at '%s': %s",
                CONFIG_PATH,
                error,
            )
        except FileNotFoundError as error:
            logging.warning(
                "Could not find directory to save config file at '%s': %s",
                CONFIG_PATH,
                error,
            )
        except OSError as error:
            if error.errno == errno.ENOSPC:
                logging.warning(
                    "No disk space to save config file at '%s': %s", CONFIG_PATH, error
                )
            else:
                logging.warning(
                    "OS error while saving config file at '%s': %s", CONFIG_PATH, error
                )
        finally:
            sys.exit(0)

    @staticmethod
    def repair_config(config: ConfigParser) -> None:
        for section, options in ConfigHandler.default_config.items():
            logging.info("Reviewing section %s for repairs...", section)
            if not config.has_section(section):
                logging.warning(
                    "Config is missing section %s, attempting repair...", section
                )
                config.add_section(section)

            for option, default_value in options.items():
                logging.info("Reviewing option %s for repairs...", option)
                if not config.has_option(section, option):
                    logging.warning(
                        "Config is missing option %s from section %s, attempting repair...",
                        option,
                        section,
                    )
                    config[section][option] = default_value
                elif not config.get(section, option).strip():
                    logging.warning(
                        "Config option %s from section %s is empty, attempting repair...",
                        option,
                        section,
                    )
                    config[section][option] = default_value

    @staticmethod
    def read_config_values(app: customtkinter.CTk) -> None:
        config = ConfigParser()
        config.read(CONFIG_PATH)

        try:
            logging.info("Starting repair review for config at '%s'", CONFIG_PATH)
            ConfigHandler.repair_config(config)
        except configparser.Error as error:
            logging.critical(
                "Error while attempting repair for config file at '%s': %s",
                CONFIG_PATH,
                error,
                exc_info=True,
            )
            sys.exit(1)

        for section in config.sections():
            section = section.upper()
            for name, value in config.items(section):
                name = name.upper()
                if (
                    section == "LANGUAGE"
                    and name == "LANGUAGE_CODE"
                    and value == "system"
                ):
                    value = locale.getdefaultlocale()[0].lower().replace("-", "_")
                logging.info("Reading option %s as %s", name, value)
                app.setvar(name, value)

    @staticmethod
    def read_config(app: customtkinter.CTk) -> None:
        try:
            if not os.path.exists(CONFIG_PATH):
                logging.info("Config file does not exist")
                raise FileNotFoundError
            ConfigHandler.read_config_values(app)
        except FileNotFoundError:
            try:
                logging.info("Creating default config...")
                ConfigHandler.create_defaults()
                ConfigHandler.read_config_values(app)
            except configparser.ParsingError as error:
                logging.critical(
                    "Error while parsing config file at '%s': %s",
                    CONFIG_PATH,
                    error,
                    exc_info=True,
                )
                sys.exit(1)
        except PermissionError as error:
            logging.critical(
                "Permission was denied while reading config file at '%s': %s",
                CONFIG_PATH,
                error,
                exc_info=True,
            )
            sys.exit(1)
        except configparser.Error as error:
            logging.critical(
                "Error while parsing config file at '%s': %s",
                CONFIG_PATH,
                error,
                exc_info=True,
            )
            sys.exit(1)
        except ValueError as error:
            logging.critical(
                "Invalid value in config file at '%s': %s",
                CONFIG_PATH,
                error,
                exc_info=True,
            )
            sys.exit(1)
        except OSError as error:
            logging.critical(
                "OS error while reading config file at '%s': %s",
                CONFIG_PATH,
                error,
                exc_info=True,
            )
            sys.exit(1)

    @staticmethod
    def create_defaults() -> None:
        default_config = ConfigParser()

        for section, options in ConfigHandler.default_config.items():
            default_config[section] = options

        with open(CONFIG_PATH, "w", encoding="utf-8") as file:
            try:
                default_config.write(file)
            except PermissionError as error:
                logging.critical(
                    "Permission was denied while creating default config file at '%s': %s",
                    CONFIG_PATH,
                    error,
                    exc_info=True,
                )
            except OSError as error:
                if error.errno == errno.ENOSPC:
                    logging.critical(
                        "No disk space to create default config file at '%s': %s",
                        CONFIG_PATH,
                        error,
                        exc_info=True,
                    )
                else:
                    logging.critical(
                        "OS error while creating default config file at '%s': %s",
                        CONFIG_PATH,
                        error,
                        exc_info=True,
                    )
