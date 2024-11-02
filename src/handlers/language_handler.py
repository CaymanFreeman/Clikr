import json
import logging
import os.path

import customtkinter
from handlers.config_handler import LANGUAGES_PATH


class LanguageHandler:
    label_keys = [
        "CHANGE_APPEARANCE_LABEL",
        "CHANGE_HOTKEY_LABEL",
        "CLICK_EVENTS_LABEL",
        "CLICK_INTERVAL_LABEL",
        "CLICK_LENGTH_LABEL",
        "CLICKS_PER_EVENT_LABEL",
        "CONFIRM_HOTKEY_LABEL",
        "HOTKEY_RECORDING_LABEL",
        "HOTKEY_LABEL",
        "LANGUAGE_LABEL",
        "LOCATION_CONFIRM_LABEL",
        "LOCATION_LABEL",
        "MOUSE_BUTTON_LABEL",
        "PICK_LOCATION_LABEL",
        "START_BUTTON_LABEL",
        "STOP_BUTTON_LABEL",
        "TITLE",
        "MILLISECONDS_CHOICE",
        "SECONDS_CHOICE",
        "MINUTES_CHOICE",
        "HOURS_CHOICE",
        "MOUSE_1_CHOICE",
        "MOUSE_2_CHOICE",
        "MOUSE_3_CHOICE",
    ]

    def __init__(self, app: customtkinter.CTk):
        self.app = app
        self.labeled_item_registry = []
        self.labels = {}
        self.languages = {}
        self.language_dropdown_choices = []
        self.scales = {}
        self.mouse_buttons = {}
        self.setup_handler()

    def setup_handler(self):
        self.labeled_item_registry = []

        self.labels = {}
        self.load_labels()

        self.languages = {}
        self.language_dropdown_choices = []
        self.load_language_names()

        self.scales = {
            "1": self.labels["MILLISECONDS_CHOICE"],
            "2": self.labels["SECONDS_CHOICE"],
            "3": self.labels["MINUTES_CHOICE"],
            "4": self.labels["HOURS_CHOICE"],
            self.labels["MILLISECONDS_CHOICE"]: "1",
            self.labels["SECONDS_CHOICE"]: "2",
            self.labels["MINUTES_CHOICE"]: "3",
            self.labels["HOURS_CHOICE"]: "4",
        }

        self.mouse_buttons = {
            "1": self.labels["MOUSE_1_CHOICE"],
            "2": self.labels["MOUSE_2_CHOICE"],
            "3": self.labels["MOUSE_3_CHOICE"],
            self.labels["MOUSE_1_CHOICE"]: "1",
            self.labels["MOUSE_2_CHOICE"]: "2",
            self.labels["MOUSE_3_CHOICE"]: "3",
        }

    def reload_labeled_items(self) -> None:
        logging.info("Reloading all labels...")
        labeled_item_registry = self.labeled_item_registry
        self.setup_handler()
        self.labeled_item_registry = labeled_item_registry
        for labeled_item in labeled_item_registry:
            labeled_item.reload()
        logging.info("Labels reloaded")

    def load_labels(self) -> None:
        logging.info("Loading labels...")
        language_file_path = os.path.join(
            LANGUAGES_PATH, self.app.getvar(name="LANGUAGE_CODE") + ".json"
        )

        fallback_file_path = os.path.join(
            LANGUAGES_PATH, self.app.getvar(name="FALLBACK_CODE") + ".json"
        )

        with open(fallback_file_path, "r", encoding="utf-8") as fallback_file, open(
            language_file_path, "r", encoding="utf-8"
        ) as language_file:
            fallback_json = json.load(fallback_file)
            language_json = json.load(language_file)

            for label_key in self.label_keys:
                self.labels[label_key] = self.get_translation(
                    language_json=language_json,
                    language_file_path=language_file_path,
                    fallback_json=fallback_json,
                    fallback_file_path=fallback_file_path,
                    key=label_key,
                )
        logging.info("Labels loaded")

    @staticmethod
    def get_translation(
        language_json,
        language_file_path,
        fallback_json,
        fallback_file_path,
        key: str,
    ) -> str:

        def attempt_fallback_translation() -> str:
            try:
                logging.info("Attempting fallback translation for key %s...", key)
                return fallback_json[key]
            except KeyError:
                logging.warning(
                    "Missing language key of %s in language file at '%s'",
                    key,
                    fallback_file_path,
                )
            except ValueError as value:
                logging.warning(
                    "Invalid language value of %s in language file at '%s'",
                    value,
                    fallback_file_path,
                )
            return "LANGUAGE_ERROR"

        try:
            return language_json[key]
        except KeyError:
            logging.warning(
                "Missing language key of %s in language file at '%s'",
                key,
                language_file_path,
            )
            return attempt_fallback_translation()
        except ValueError as value:
            logging.warning(
                "Invalid language value of %s in language file at '%s'",
                value,
                language_file_path,
            )
            return attempt_fallback_translation()

    def load_language_names(self) -> None:
        logging.info("Scanning for languages...")
        language_count = 0
        for file_name in os.listdir(LANGUAGES_PATH):
            if file_name.endswith(".json"):
                try:
                    with open(
                        os.path.join(LANGUAGES_PATH, file_name), "r", encoding="utf-8"
                    ) as file:
                        file_json = json.load(file)
                        self.languages[file_json["LANGUAGE"]] = file_name.removesuffix(
                            ".json"
                        )
                        self.languages[file_name.removesuffix(".json")] = file_json[
                            "LANGUAGE"
                        ]
                        self.language_dropdown_choices.append(file_json["LANGUAGE"])
                    language_count += 1
                except KeyError:
                    pass
        self.language_dropdown_choices = sorted(self.language_dropdown_choices)
        logging.info("Found %d languages", language_count)
