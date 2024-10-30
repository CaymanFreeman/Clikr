import json
import os.path

import customtkinter

from config_handler import LANGUAGES_PATH


class LabelVariables:
    def __init__(self, app: customtkinter.CTk):
        language_file = os.path.join(LANGUAGES_PATH, app.getvar(name="LANGUAGE_CODE") + ".json")
        with open(language_file, "r", encoding='utf-8') as file:
            language_json = json.load(file)
            self.CHANGE_APPEARANCE_LABEL = self.get_translation(language_json=language_json, key="CHANGE_APPEARANCE_LABEL")
            self.CHANGE_HOTKEY_LABEL = self.get_translation(language_json=language_json, key="CHANGE_HOTKEY_LABEL")
            self.CLICK_EVENTS_LABEL = self.get_translation(language_json=language_json, key="CLICK_EVENTS_LABEL")
            self.CLICK_INTERVAL_LABEL = self.get_translation(language_json=language_json, key="CLICK_INTERVAL_LABEL")
            self.CLICK_LENGTH_LABEL = self.get_translation(language_json=language_json, key="CLICK_LENGTH_LABEL")
            self.CLICKS_PER_EVENT_LABEL = self.get_translation(language_json=language_json, key="CLICKS_PER_EVENT_LABEL")
            self.CONFIRM_HOTKEY_LABEL = self.get_translation(language_json=language_json, key="CONFIRM_HOTKEY_LABEL")
            self.HOTKEY_RECORDING_LABEL = self.get_translation(language_json=language_json, key="HOTKEY_RECORDING_LABEL")
            self.HOTKEY_LABEL = self.get_translation(language_json=language_json, key="HOTKEY_LABEL")
            self.LOCATION_CONFIRM_LABEL = self.get_translation(language_json=language_json, key="LOCATION_CONFIRM_LABEL")
            self.LOCATION_LABEL = self.get_translation(language_json=language_json, key="LOCATION_LABEL")
            self.MOUSE_BUTTON_LABEL = self.get_translation(language_json=language_json, key="MOUSE_BUTTON_LABEL")
            self.PICK_LOCATION_LABEL = self.get_translation(language_json=language_json, key="PICK_LOCATION_LABEL")
            self.START_BUTTON_LABEL = self.get_translation(language_json=language_json, key="START_BUTTON_LABEL")
            self.STOP_BUTTON_LABEL = self.get_translation(language_json=language_json, key="STOP_BUTTON_LABEL")
            self.TITLE = self.get_translation(language_json=language_json, key="TITLE")
            self.MILLISECONDS_CHOICE = self.get_translation(language_json=language_json, key="MILLISECONDS_CHOICE")
            self.SECONDS_CHOICE = self.get_translation(language_json=language_json, key="SECONDS_CHOICE")
            self.MINUTES_CHOICE = self.get_translation(language_json=language_json, key="MINUTES_CHOICE")
            self.HOURS_CHOICE = self.get_translation(language_json=language_json, key="HOURS_CHOICE")
            self.MOUSE_1_CHOICE = self.get_translation(language_json=language_json, key="MOUSE_1_CHOICE")
            self.MOUSE_2_CHOICE = self.get_translation(language_json=language_json, key="MOUSE_2_CHOICE")
            self.MOUSE_3_CHOICE = self.get_translation(language_json=language_json, key="MOUSE_3_CHOICE")
    
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

def translate_scale(label_variables: LabelVariables, scale: str) -> str:
    match scale:
        case "1":
            return label_variables.MILLISECONDS_CHOICE
        case "2":
            return label_variables.SECONDS_CHOICE
        case "3":
            return label_variables.MINUTES_CHOICE
        case "4":
            return label_variables.HOURS_CHOICE

def detranslate_scale(label_variables: LabelVariables, scale: str) -> str:
    match scale:
        case label_variables.MILLISECONDS_CHOICE:
            return "1"
        case label_variables.SECONDS_CHOICE:
            return "2"
        case label_variables.MINUTES_CHOICE:
            return "3"
        case label_variables.HOURS_CHOICE:
            return "4"

def translate_mouse_button(label_variables: LabelVariables, button: str) -> str:
    match button:
        case "1":
            return label_variables.MOUSE_1_CHOICE
        case "2":
            return label_variables.MOUSE_2_CHOICE
        case "3":
            return label_variables.MOUSE_3_CHOICE

def detranslate_mouse_button(label_variables: LabelVariables, button: str) -> str:
    match button:
        case label_variables.MOUSE_1_CHOICE:
            return "1"
        case label_variables.MOUSE_2_CHOICE:
            return "2"
        case label_variables.MOUSE_3_CHOICE:
            return "3"
