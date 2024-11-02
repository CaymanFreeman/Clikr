import json
import logging
from typing import Union

from handlers.config_handler import THEME_PATH


class AppearanceHandler:
    def __init__(self):
        with open(THEME_PATH, "r", encoding="utf-8") as file:
            theme_json = json.load(file)
            self.label_text_color = AppearanceHandler.to_color_variable(
                theme_json["CTkLabel"]["text_color"]
            )
            self.label_text_disabled_color = AppearanceHandler.to_color_variable(
                theme_json["CTkLabel"]["text_color_disabled"]
            )
            self.button_text_color = AppearanceHandler.to_color_variable(
                theme_json["CTkButton"]["text_color"]
            )
            self.button_disabled_color = AppearanceHandler.to_color_variable(
                theme_json["CTkButton"]["disabled_color"]
            )
            self.button_fg_color = AppearanceHandler.to_color_variable(
                theme_json["CTkButton"]["fg_color"]
            )
            self.button_confirm_fg_color = AppearanceHandler.to_color_variable(
                theme_json["CTkButton"]["confirm_fg_color"]
            )
            self.button_hover_color = AppearanceHandler.to_color_variable(
                theme_json["CTkButton"]["hover_color"]
            )
            self.button_confirm_hover_color = AppearanceHandler.to_color_variable(
                theme_json["CTkButton"]["confirm_hover_color"]
            )

    @staticmethod
    def to_color_variable(json_setting: Union[list, str]) -> Union[tuple, str]:
        if isinstance(json_setting, list):
            if len(json_setting) > 2:
                logging.warning(
                    "Color value of %s has %d elements (max 2) in theme file at '%s'",
                    json_setting,
                    len(json_setting),
                    THEME_PATH,
                )
                return tuple(json_setting[:2])
            if len(json_setting) == 2:
                return tuple(json_setting)
            if len(json_setting) == 1:
                return json_setting[0]
        elif isinstance(json_setting, str):
            return json_setting
        else:
            logging.warning(
                "Invalid color value of %s (%s) in theme file at '%s'",
                json_setting,
                type(json_setting),
                THEME_PATH,
            )
        return "#FF69B4"
