"""Provides input management and processing for the Clikr UI and click worker."""

import logging
from enum import IntEnum
from typing import Optional, Callable, Any

from PyQt6.QtWidgets import QLineEdit, QComboBox, QKeySequenceEdit, QPushButton
from pynput.keyboard import (
    Key,
    Listener as KeyboardListener,
    HotKey,
    KeyCode,
)
from pynput.mouse import (
    Button as MouseButton,
    Controller as MouseController,
    Listener as MouseListener,
)

from src.core.click_worker import WorkerInputs


class InputTimescale(IntEnum):
    """Enum for the supported time scales of inputs."""

    MILLISECONDS = 0
    SECONDS = 1
    MINUTES = 2
    HOURS = 3


class ChangeLocationListener:
    """Handles mouse position capture for setting click locations."""

    def __init__(
        self,
        change_location_callback: Callable[[int, int], None],
        change_location_button: Callable[[], QPushButton],
    ) -> None:
        self.__change_location_callback: Callable[[int, int], None] = (
            change_location_callback
        )
        self.__change_location_button: Callable[[], QPushButton] = (
            change_location_button
        )
        self.__change_location_listener: Optional[MouseListener] = None
        self.__cancel_key_listener: Optional[KeyboardListener] = None
        self.__cancel_key: Key = Key.esc

    def start(self) -> None:
        """Starts listening for a new location click or the cancellation key."""
        self.__change_location_button().setEnabled(False)

        def change_location(x: int, y: int, _: MouseButton, pressed: bool) -> None:
            """Stops listening and changes the location setting if the mouse clicks."""
            if pressed:
                self.__change_location_callback(x, y)
                self.stop()

        def cancel_change(key: Key | KeyCode | None) -> None:
            """Stops listening if the cancel key is pressed."""
            if key == self.__cancel_key:
                self.stop()

        self.__cancel_key_listener = KeyboardListener(on_press=cancel_change)
        self.__cancel_key_listener.start()
        logging.debug("Started cancellation key listener")

        self.__change_location_listener = MouseListener(on_click=change_location)
        self.__change_location_listener.start()
        logging.debug("Started change location click listener")

    def stop(self) -> None:
        """Stops listening for a new location click and the cancellation key."""
        if self.__change_location_listener:
            self.__change_location_listener.stop()
            self.__change_location_listener = None
            logging.debug("Stopped change location click listener")

        if self.__cancel_key_listener:
            self.__cancel_key_listener.stop()
            self.__cancel_key_listener = None
            logging.debug("Stopped cancellation key listener")

        self.__change_location_button().setEnabled(True)


class HotkeyListener:
    """Handles hotkey detection and execution."""

    def __init__(
        self, hotkey_callback: Callable[[], None], hotkey: Callable[[], Optional[str]]
    ) -> None:
        self.__hotkey_callback = hotkey_callback
        self.__hotkey = hotkey
        self.__hotkey_listener: Optional[KeyboardListener] = None

    def reset(self) -> None:
        """Restarts the hotkey listener to update to the current hotkey."""
        self.stop()
        self.start()

    def start(self) -> None:
        """Starts listening for current hotkey."""
        hotkey = self.__hotkey()
        if hotkey is not None:

            def for_canonical(
                function: Callable[[Key | KeyCode | Any], None]
            ) -> Callable[[Key | KeyCode | Any], None]:
                return lambda key_event: function(
                    self.__hotkey_listener.canonical(key_event)
                )

            pynput_hotkey = HotKey(HotKey.parse(hotkey), self.__hotkey_callback)
            self.__hotkey_listener = KeyboardListener(
                on_press=for_canonical(pynput_hotkey.press),
                on_release=for_canonical(pynput_hotkey.release),
            )
            self.__hotkey_listener.start()
            logging.debug("Started hotkey listener for %s", hotkey)

    def stop(self) -> None:
        """Stops listening for current hotkey."""
        if self.__hotkey_listener:
            self.__hotkey_listener.stop()
            self.__hotkey_listener = None
            logging.debug("Stopped hotkey listener")


class InputManager:
    """Handles input management and processing for Clikr."""

    DEFAULT_INTERVAL_SECONDS: int = 100
    DEFAULT_INTERVAL_TIMESCALE: InputTimescale = InputTimescale.MILLISECONDS
    DEFAULT_HOLD_LENGTH_SECONDS: int = 0
    DEFAULT_HOLD_LENGTH_TIMESCALE: InputTimescale = InputTimescale.MILLISECONDS
    DEFAULT_CLICKS_PER_EVENT: int = 1
    DEFAULT_EVENT_COUNT: Optional[int] = None
    DEFAULT_LOCATION: tuple[Optional[int], Optional[int]] = None, None
    DEFAULT_MOUSE_BUTTON: MouseButton = MouseButton.left
    DEFAULT_HOTKEY: Optional[str] = None

    @classmethod
    def _scale_seconds(cls, timescale: InputTimescale, unscaled_value: int) -> float:
        """Returns the scaled value based on the timescale."""
        match timescale:
            case InputTimescale.MILLISECONDS:
                return 0.001 * unscaled_value
            case InputTimescale.SECONDS:
                return 1.0 * unscaled_value
            case InputTimescale.MINUTES:
                return 60.0 * unscaled_value
            case InputTimescale.HOURS:
                return 3600.0 * unscaled_value

    def __init__(
        self,
        change_location_callback: Callable[[int, int], None],
        change_location_button: Callable[[], QPushButton],
        hotkey_callback: Callable[[], None],
    ):
        self.__unscaled_interval: int = self.DEFAULT_INTERVAL_SECONDS
        self.__interval_timescale: InputTimescale = self.DEFAULT_INTERVAL_TIMESCALE
        self.__unscaled_hold_length: int = self.DEFAULT_HOLD_LENGTH_SECONDS
        self.__hold_length_timescale: InputTimescale = (
            self.DEFAULT_HOLD_LENGTH_TIMESCALE
        )
        self.__clicks_per_event: int = self.DEFAULT_CLICKS_PER_EVENT
        self.__event_count: Optional[int] = self.DEFAULT_EVENT_COUNT
        self.__location: tuple[Optional[int], Optional[int]] = self.DEFAULT_LOCATION
        self.__mouse_button: MouseButton = self.DEFAULT_MOUSE_BUTTON
        self.__hotkey: Optional[str] = self.DEFAULT_HOTKEY

        self.__mouse_controller: MouseController = MouseController()
        self.__change_location_listener: ChangeLocationListener = (
            ChangeLocationListener(change_location_callback, change_location_button)
        )
        self.__hotkey_listener: HotkeyListener = HotkeyListener(
            hotkey_callback, self.hotkey_callable
        )

    @property
    def interval(self) -> float:
        """Returns the current interval scaled to seconds."""
        return self._scale_seconds(self.__interval_timescale, self.__unscaled_interval)

    def update_unscaled_interval(self, line_edit: QLineEdit) -> None:
        """Sets the unscaled interval based on the provided input field."""
        interval_seconds: int = self.DEFAULT_INTERVAL_SECONDS
        if line_edit.text():
            interval_seconds = int(line_edit.text())
        self.__unscaled_interval = interval_seconds
        logging.debug("Set unscaled interval to %f", interval_seconds)

    def update_interval_timescale(self, combo_box: QComboBox) -> None:
        """Sets the interval timescale based on the provided input choice."""
        interval_timescale = InputTimescale(combo_box.currentIndex())
        self.__interval_timescale = interval_timescale
        logging.debug("Set interval timescale to %s", interval_timescale.name)

    @property
    def hold_length(self) -> float:
        """Returns the current hold length scaled to seconds."""
        return self._scale_seconds(
            self.__hold_length_timescale, self.__unscaled_hold_length
        )

    @property
    def is_using_held_clicks(self) -> bool:
        """Returns whether the current hold length constitutes held clicks."""
        return self.hold_length > 0

    def update_unscaled_hold_length(self, line_edit: QLineEdit) -> None:
        """Sets the unscaled hold length based on the provided input field."""
        hold_length_seconds: int = self.DEFAULT_HOLD_LENGTH_SECONDS
        if line_edit.text():
            hold_length_seconds = int(line_edit.text())
        self.__unscaled_hold_length = hold_length_seconds
        logging.debug("Set unscaled hold length to %f", hold_length_seconds)

    def update_hold_length_timescale(self, combo_box: QComboBox) -> None:
        """Sets the hold length timescale based on the provided input choice."""
        hold_length_timescale = InputTimescale(combo_box.currentIndex())
        self.__hold_length_timescale = hold_length_timescale
        logging.debug("Set hold length timescale to %s", hold_length_timescale.name)

    def update_clicks_per_event(self, line_edit: QLineEdit) -> None:
        """Sets the number of clicks for each event based on the provided input field."""
        clicks_per_event: int = self.DEFAULT_CLICKS_PER_EVENT
        if line_edit.text():
            clicks_per_event = int(line_edit.text())
        self.__clicks_per_event = clicks_per_event
        logging.debug("Set clicks per event to %s", clicks_per_event)

    def update_event_count(self, line_edit: QLineEdit) -> None:
        """Sets the number of events to perform based on the provided input field."""
        event_count: Optional[int] = self.DEFAULT_EVENT_COUNT
        if line_edit.text():
            event_count = int(line_edit.text())
        self.__event_count = event_count
        logging.debug("Set event count to %s", event_count)

    @property
    def is_continuous(self) -> bool:
        """Returns whether the current inputs constitute clicking forever if not stopped."""
        return self.__event_count is None

    @property
    def location_x(self) -> Optional[int]:
        """Returns the X component of the current location."""
        return self.__location[0]

    def update_location_x(self, line_edit: QLineEdit) -> None:
        """Sets the X component of the current location based on the provided input field."""
        _, y = self.__location
        if line_edit.text():
            self.__location = int(line_edit.text()), y
        else:
            self.__location = None, y
        logging.debug("Set X location to %s", self.location_x)

    @property
    def location_y(self) -> Optional[int]:
        """Returns the Y component of the current location."""
        return self.__location[1]

    def update_location_y(self, line_edit: QLineEdit) -> None:
        """Sets the Y component of the current location based on the provided input field."""
        x, _ = self.__location
        if line_edit.text():
            self.__location = x, int(line_edit.text())
        else:
            self.__location = x, None
        logging.debug("Set Y location to %s", self.location_y)

    def update_mouse_button(self, combo_box: QComboBox) -> None:
        """Sets the mouse button to click with based on the provided input choice."""
        mouse_button = MouseButton(combo_box.currentIndex() + 1)
        self.__mouse_button = mouse_button
        logging.debug("Set mouse button to %s", mouse_button.name)

    def update_hotkey(self, key_sequence_edit: QKeySequenceEdit) -> None:
        """
        Sets the current hotkey based on the provided input field.
        Converts from a PyQt key sequence format to a pynput hotkey format.
        """
        hotkey: Optional[str] = self.DEFAULT_HOTKEY
        key_sequence: str = key_sequence_edit.keySequence().toString().strip()
        if key_sequence:
            keys: list[str] = [
                f"<{key}>" for key in key_sequence.split("+") if len(key) > 1
            ]
            hotkey = "+".join(keys)
        self.__hotkey = hotkey
        logging.debug("Set hotkey to %s", hotkey)
        self.__hotkey_listener.reset()

    def hotkey_callable(self) -> Optional[str]:
        """Returns the current hotkey in pynput format as a non-property to act as a callable."""
        return self.__hotkey

    @property
    def worker_inputs(self) -> WorkerInputs:
        """Returns the current input configuration needed for a click worker."""
        return WorkerInputs(
            self.interval,
            self.hold_length,
            self.__clicks_per_event,
            self.__event_count,
            self.__mouse_button,
            self.__location,
            self.location_x is not None,
            self.location_y is not None,
            self.hold_length > 0,
            self.__event_count is None,
            self.__mouse_controller,
        )

    @property
    def can_softlock(self) -> bool:
        """Returns whether to show the softlock prevention pop-up."""
        return (
            self.location_x is not None or self.location_y is not None
        ) and self.__hotkey is None

    def listen_for_location(self) -> None:
        """Starts the change location listener."""
        self.__change_location_listener.start()
