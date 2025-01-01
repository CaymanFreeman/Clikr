import logging
from collections import namedtuple
from enum import IntEnum
from typing import Optional, Callable

from PyQt6.QtWidgets import QLineEdit, QComboBox, QKeySequenceEdit, QPushButton
from pynput import mouse, keyboard
from pynput.mouse import Controller as MouseController
from pynput.mouse import Button


class InputTimescale(IntEnum):
    Milliseconds = 0
    Seconds = 1
    Minutes = 2
    Hours = 3


class ChangeLocationListener:
    def __init__(
        self,
        change_location_callback: Callable[[int, int], None],
        change_location_button: Callable[[], QPushButton],
    ):
        self.__change_location_callback: Callable[[int, int], None] = (
            change_location_callback
        )
        self.__change_location_button: Callable[[], QPushButton] = (
            change_location_button
        )
        self.__change_location_listener: Optional[mouse.Listener] = None
        self.__change_location_escape_listener: Optional[keyboard.Listener] = None

    def start(self):
        self.__change_location_button().setEnabled(False)
        self.__change_location_listener = mouse.Listener(
            on_click=self.__on_change_location
        )
        self.__change_location_escape_listener = keyboard.Listener(
            on_press=self.__on_esc_change_location
        )
        self.__change_location_listener.start()
        self.__change_location_escape_listener.start()
        logging.debug("Started change location listeners")

    def stop(self):
        if self.__change_location_listener:
            self.__change_location_listener.stop()
            self.__change_location_listener = None
        if self.__change_location_escape_listener:
            self.__change_location_escape_listener.stop()
            self.__change_location_escape_listener = None
        self.__change_location_button().setEnabled(True)
        logging.debug("Stopped change location listeners")

    def __on_change_location(self, x: int, y: int, button: Button, pressed: bool):
        if pressed:
            self.__change_location_callback(x, y)
            self.stop()

    def __on_esc_change_location(self, key: keyboard.Key):
        if key == keyboard.Key.esc:
            self.stop()


class HotkeyListener:
    def __init__(self, hotkey_callback: Callable[[], None], hotkey: Callable[[], str]):
        self.__hotkey = hotkey
        self.__hotkey_callback = hotkey_callback
        self.__hotkey_listener: Optional[keyboard.Listener] = None

    def reset(self):
        self.__stop()
        self.__start()

    def __start(self):
        hotkey = self.__hotkey()
        if hotkey:

            def for_canonical(f):
                return lambda k: f(self.__hotkey_listener.canonical(k))

            pynput_hotkey = keyboard.HotKey(
                keyboard.HotKey.parse(hotkey), self.__hotkey_callback
            )
            self.__hotkey_listener = keyboard.Listener(
                on_press=for_canonical(pynput_hotkey.press),
                on_release=for_canonical(pynput_hotkey.release),
            )
            self.__hotkey_listener.start()
            logging.debug(f"Started hotkey listener for {hotkey}")

    def __stop(self):
        if self.__hotkey_listener:
            self.__hotkey_listener.stop()
            self.__hotkey_listener = None
            logging.debug("Stopped hotkey listener")


class InputManager:

    DEFAULT_INTERVAL_SECONDS: int = 100
    DEFAULT_INTERVAL_TIMESCALE: InputTimescale = InputTimescale.Milliseconds
    DEFAULT_HOLD_LENGTH_SECONDS: int = 0
    DEFAULT_HOLD_LENGTH_TIMESCALE: InputTimescale = InputTimescale.Milliseconds
    DEFAULT_CLICKS_PER_EVENT: int = 1
    DEFAULT_EVENT_COUNT: Optional[int] = None
    DEFAULT_LOCATION: tuple[Optional[int], Optional[int]] = None, None
    DEFAULT_MOUSE_BUTTON: Button = Button.left
    DEFAULT_HOTKEY: Optional[str] = None

    WorkerInputs = namedtuple(
        "WorkerInputs",
        [
            "interval",
            "hold_length",
            "clicks_per_event",
            "event_count",
            "mouse_button",
            "location",
            "is_using_location_x",
            "is_using_location_y",
            "is_using_held_clicks",
            "is_continuous",
            "mouse_controller",
        ],
    )

    @classmethod
    def __scale_seconds(cls, timescale: InputTimescale, seconds: int) -> float:
        match timescale:
            case InputTimescale.Milliseconds:
                return 0.001 * seconds
            case InputTimescale.Seconds:
                return 1.0 * seconds
            case InputTimescale.Minutes:
                return 60.0 * seconds
            case InputTimescale.Hours:
                return 3600.0 * seconds

    def __init__(
        self,
        change_location_callback: Callable[[int, int], None],
        change_location_button: Callable[[], QPushButton],
        hotkey_callback: Callable[[], None],
    ):
        self.__interval_seconds: int = self.DEFAULT_INTERVAL_SECONDS
        self.__interval_timescale: InputTimescale = self.DEFAULT_INTERVAL_TIMESCALE
        self.__hold_length_seconds: int = self.DEFAULT_HOLD_LENGTH_SECONDS
        self.__hold_length_timescale: InputTimescale = (
            self.DEFAULT_HOLD_LENGTH_TIMESCALE
        )
        self.__clicks_per_event: int = self.DEFAULT_CLICKS_PER_EVENT
        self.__event_count: Optional[int] = self.DEFAULT_EVENT_COUNT
        self.__location: Optional[tuple[int, int]] = self.DEFAULT_LOCATION
        self.__mouse_button: Button = self.DEFAULT_MOUSE_BUTTON
        self.__hotkey: Optional[str] = self.DEFAULT_HOTKEY

        self.__mouse_controller: MouseController = mouse.Controller()
        self.__change_location_listener: ChangeLocationListener = (
            ChangeLocationListener(change_location_callback, change_location_button)
        )
        self.__hotkey_listener: HotkeyListener = HotkeyListener(
            hotkey_callback, self.hotkey_callable
        )

    @property
    def __interval(self) -> float:
        return self.__scale_seconds(self.__interval_timescale, self.__interval_seconds)

    @property
    def interval_seconds(self) -> int:
        return self.__interval_seconds

    @interval_seconds.setter
    def interval_seconds(self, line_edit: QLineEdit):
        interval_seconds: int = self.DEFAULT_INTERVAL_SECONDS
        if line_edit.text():
            interval_seconds = int(line_edit.text())
        self.__interval_seconds = interval_seconds
        logging.debug(f"Set interval seconds to {interval_seconds}")

    @property
    def interval_timescale(self) -> InputTimescale:
        return self.__interval_timescale

    @interval_timescale.setter
    def interval_timescale(self, combo_box: QComboBox):
        interval_timescale = InputTimescale(combo_box.currentIndex())
        self.__interval_timescale = interval_timescale
        logging.debug(f"Set interval timescale to {interval_timescale}")

    @property
    def __is_using_held_clicks(self) -> bool:
        return self.__hold_length > 0

    @property
    def __hold_length(self) -> float:
        return self.__scale_seconds(
            self.__hold_length_timescale, self.__hold_length_seconds
        )

    @property
    def hold_length_seconds(self) -> int:
        return self.__hold_length_seconds

    @hold_length_seconds.setter
    def hold_length_seconds(self, line_edit: QLineEdit):
        hold_length_seconds: int = self.DEFAULT_HOLD_LENGTH_SECONDS
        if line_edit.text():
            hold_length_seconds = int(line_edit.text())
        self.__hold_length_seconds = hold_length_seconds
        logging.debug(f"Set hold length seconds to {hold_length_seconds}")

    @property
    def hold_length_timescale(self) -> InputTimescale:
        return self.__hold_length_timescale

    @hold_length_timescale.setter
    def hold_length_timescale(self, combo_box: QComboBox):
        hold_length_timescale = InputTimescale(combo_box.currentIndex())
        self.__hold_length_timescale = hold_length_timescale
        logging.debug(f"Set hold length timescale to {hold_length_timescale}")

    @property
    def clicks_per_event(self) -> int:
        return self.__clicks_per_event

    @clicks_per_event.setter
    def clicks_per_event(self, line_edit: QLineEdit):
        clicks_per_event: int = self.DEFAULT_CLICKS_PER_EVENT
        if line_edit.text():
            clicks_per_event = int(line_edit.text())
        self.__clicks_per_event = clicks_per_event
        logging.debug(f"Set clicks per event to {clicks_per_event}")

    @property
    def event_count(self) -> int:
        return self.__event_count

    @event_count.setter
    def event_count(self, line_edit: QLineEdit):
        event_count: Optional[int] = self.DEFAULT_EVENT_COUNT
        if line_edit.text():
            event_count = int(line_edit.text())
        self.__event_count = event_count
        logging.debug(f"Set event count to {event_count}")

    @property
    def __is_continuous(self) -> bool:
        return self.__event_count is None

    @property
    def location_x(self) -> int:
        return self.__location[0]

    @location_x.setter
    def location_x(self, line_edit: QLineEdit):
        if line_edit.text():
            self.__location = int(line_edit.text()), self.__location[1]
        else:
            self.__location = None, self.__location[1]
        logging.debug(f"Set X location to {self.__location[0]}")

    @property
    def location_y(self) -> int:
        return self.__location[1]

    @location_y.setter
    def location_y(self, line_edit: QLineEdit):
        if line_edit.text():
            self.__location = self.__location[0], int(line_edit.text())
        else:
            self.__location = self.__location[0], None
        logging.debug(f"Set Y location to {self.__location[1]}")

    @property
    def __is_using_location_x(self) -> bool:
        return self.__location[0] is not None

    @property
    def __is_using_location_y(self) -> bool:
        return self.__location[1] is not None

    @property
    def mouse_button(self) -> Button:
        return self.__mouse_button

    @mouse_button.setter
    def mouse_button(self, combo_box: QComboBox):
        mouse_button = Button(combo_box.currentIndex() + 1)
        self.__mouse_button = mouse_button
        logging.debug(f"Set mouse button to {mouse_button}")

    @property
    def hotkey(self) -> str:
        return self.__hotkey

    def hotkey_callable(self) -> str:
        return self.hotkey

    @hotkey.setter
    def hotkey(self, key_sequence_edit: QKeySequenceEdit):
        hotkey: Optional[str] = self.DEFAULT_HOTKEY
        key_sequence: str = key_sequence_edit.keySequence().toString().strip()
        if key_sequence:
            keys: list[str] = key_sequence.split("+")
            for index in range(len(keys)):
                if len(keys[index]) > 1:
                    keys[index] = f"<{keys[index]}>"
            hotkey = "+".join(keys)
        self.__hotkey = hotkey
        logging.debug(f"Set hotkey to {hotkey}")
        self.__hotkey_listener.reset()

    @property
    def worker_inputs(self) -> WorkerInputs:
        return self.WorkerInputs(
            self.__interval,
            self.__hold_length,
            self.__clicks_per_event,
            self.__event_count,
            self.__mouse_button,
            self.__location,
            self.__is_using_location_x,
            self.__is_using_location_y,
            self.__is_using_held_clicks,
            self.__is_continuous,
            self.__mouse_controller,
        )

    @property
    def can_softlock(self) -> bool:
        return (
            self.__is_using_location_x or self.__is_using_location_y
        ) and self.__hotkey is None

    def change_location(self):
        self.__change_location_listener.start()
