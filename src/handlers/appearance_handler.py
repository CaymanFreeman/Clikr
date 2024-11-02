import json
from typing import Union

from handlers.config_handler import THEME_PATH


class AppearanceHandler:
    def __init__(self):
        with open(THEME_PATH, "r") as file:
            theme_json = json.load(file)
            self.LABEL_TEXT_COLOR = AppearanceHandler.to_variable(
                theme_json["CTkLabel"]["text_color"]
            )
            self.LABEL_TEXT_DISABLED_COLOR = AppearanceHandler.to_variable(
                theme_json["CTkLabel"]["text_color_disabled"]
            )
            self.BUTTON_TEXT_COLOR = AppearanceHandler.to_variable(
                theme_json["CTkButton"]["text_color"]
            )
            self.BUTTON_DISABLED_COLOR = AppearanceHandler.to_variable(
                theme_json["CTkButton"]["disabled_color"]
            )
            self.BUTTON_FG_COLOR = AppearanceHandler.to_variable(
                theme_json["CTkButton"]["fg_color"]
            )
            self.BUTTON_CONFIRM_FG_COLOR = AppearanceHandler.to_variable(
                theme_json["CTkButton"]["confirm_fg_color"]
            )
            self.BUTTON_HOVER_COLOR = AppearanceHandler.to_variable(
                theme_json["CTkButton"]["hover_color"]
            )
            self.BUTTON_CONFIRM_HOVER_COLOR = AppearanceHandler.to_variable(
                theme_json["CTkButton"]["confirm_hover_color"]
            )

    @staticmethod
    def to_variable(json_setting: Union[list, tuple, str]) -> Union[tuple, str]:
        if isinstance(json_setting, list):
            if len(json_setting) > 2:
                print(
                    f"Json setting list too long: {json_setting} has {len(json_setting)} elements"
                )
            elif len(json_setting) == 2:
                return tuple(json_setting)
            elif len(json_setting) == 1:
                return json_setting[0]
        elif isinstance(json_setting, str):
            return json_setting
        else:
            print(
                f"Invalid json setting type: {json_setting} as a {type(json_setting)}"
            )
