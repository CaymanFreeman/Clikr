import json
import os.path

import customtkinter

from handlers.config_handler import LANGUAGES_PATH


class LanguageHandler:
    def __init__(self, app: customtkinter.CTk):
        self.app = app

        self.labeled_item_registry = []

        language_file = os.path.join(LANGUAGES_PATH, app.getvar(name="LANGUAGE_CODE") + ".json")
        with open(language_file, "r", encoding="utf-8") as file:
            language_json = json.load(file)
            self.labels = {
                "CHANGE_APPEARANCE_LABEL": self.get_translation(language_json=language_json,
                                                                key="CHANGE_APPEARANCE_LABEL"),
                "CHANGE_HOTKEY_LABEL": self.get_translation(language_json=language_json, key="CHANGE_HOTKEY_LABEL"),
                "CLICK_EVENTS_LABEL": self.get_translation(language_json=language_json, key="CLICK_EVENTS_LABEL"),
                "CLICK_INTERVAL_LABEL": self.get_translation(language_json=language_json, key="CLICK_INTERVAL_LABEL"),
                "CLICK_LENGTH_LABEL": self.get_translation(language_json=language_json, key="CLICK_LENGTH_LABEL"),
                "CLICKS_PER_EVENT_LABEL": self.get_translation(language_json=language_json,
                                                               key="CLICKS_PER_EVENT_LABEL"),
                "CONFIRM_HOTKEY_LABEL": self.get_translation(language_json=language_json, key="CONFIRM_HOTKEY_LABEL"),
                "HOTKEY_RECORDING_LABEL": self.get_translation(language_json=language_json,
                                                               key="HOTKEY_RECORDING_LABEL"),
                "HOTKEY_LABEL": self.get_translation(language_json=language_json, key="HOTKEY_LABEL"),
                "LANGUAGE_LABEL": self.get_translation(language_json=language_json, key="LANGUAGE_LABEL"),
                "LOCATION_CONFIRM_LABEL": self.get_translation(language_json=language_json,
                                                               key="LOCATION_CONFIRM_LABEL"),
                "LOCATION_LABEL": self.get_translation(language_json=language_json, key="LOCATION_LABEL"),
                "MOUSE_BUTTON_LABEL": self.get_translation(language_json=language_json, key="MOUSE_BUTTON_LABEL"),
                "PICK_LOCATION_LABEL": self.get_translation(language_json=language_json, key="PICK_LOCATION_LABEL"),
                "START_BUTTON_LABEL": self.get_translation(language_json=language_json, key="START_BUTTON_LABEL"),
                "STOP_BUTTON_LABEL": self.get_translation(language_json=language_json, key="STOP_BUTTON_LABEL"),
                "TITLE": self.get_translation(language_json=language_json, key="TITLE"),
                "MILLISECONDS_CHOICE": self.get_translation(language_json=language_json, key="MILLISECONDS_CHOICE"),
                "SECONDS_CHOICE": self.get_translation(language_json=language_json, key="SECONDS_CHOICE"),
                "MINUTES_CHOICE": self.get_translation(language_json=language_json, key="MINUTES_CHOICE"),
                "HOURS_CHOICE": self.get_translation(language_json=language_json, key="HOURS_CHOICE"),
                "MOUSE_1_CHOICE": self.get_translation(language_json=language_json, key="MOUSE_1_CHOICE"),
                "MOUSE_2_CHOICE": self.get_translation(language_json=language_json, key="MOUSE_2_CHOICE"),
                "MOUSE_3_CHOICE": self.get_translation(language_json=language_json, key="MOUSE_3_CHOICE")
            }

        self.languages = {}
        self.language_choices = []
        self.load_language_names()

        self.scales = {
            "1": self.labels["MILLISECONDS_CHOICE"],
            "2": self.labels["SECONDS_CHOICE"],
            "3": self.labels["MINUTES_CHOICE"],
            "4": self.labels["HOURS_CHOICE"],
            self.labels["MILLISECONDS_CHOICE"]: "1",
            self.labels["SECONDS_CHOICE"]: "2",
            self.labels["MINUTES_CHOICE"]: "3",
            self.labels["HOURS_CHOICE"]: "4"
        }

        self.mouse_buttons = {
            "1": self.labels["MOUSE_1_CHOICE"],
            "2": self.labels["MOUSE_2_CHOICE"],
            "3": self.labels["MOUSE_3_CHOICE"],
            self.labels["MOUSE_1_CHOICE"]: "1",
            self.labels["MOUSE_2_CHOICE"]: "2",
            self.labels["MOUSE_3_CHOICE"]: "3"
        }

    def reload_labeled_items(self):
        labeled_item_registry = self.labeled_item_registry
        self.__init__(self.app)
        self.labeled_item_registry = labeled_item_registry
        for labeled_item in labeled_item_registry:
            labeled_item.reload()

    @staticmethod
    def get_translation(language_json, key: str) -> str:
        try:
            return language_json[key]
        except Exception as error:
            print(f"Encountered translation error with: {error}\nAttempting fallback...")
            try:
                with open(os.path.join(LANGUAGES_PATH, "en_us.json"), "r") as file:
                    en_us_json = json.load(file)
                    return en_us_json[key]
            except Exception as error:
                print(f"Translation error: {error}")

    def load_language_names(self) -> None:
        for file_name in os.listdir(LANGUAGES_PATH):
            if file_name.endswith(".json"):
                with open(os.path.join(LANGUAGES_PATH, file_name), "r", encoding="utf-8") as file:
                    file_json = json.load(file)
                    self.languages[file_json["LANGUAGE"]] = file_name.removesuffix(".json")
                    self.languages[file_name.removesuffix(".json")] = file_json["LANGUAGE"]
                    self.language_choices.append(file_json["LANGUAGE"])
        self.language_choices = sorted(self.language_choices)
