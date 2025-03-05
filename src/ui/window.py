# Copyright (C) 2025  Cayman Freeman
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Provides the PyQt window for Clikr."""

import logging
import os
import sys
from pathlib import Path
from typing import Optional, override

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QIntValidator, QKeyEvent
from PyQt6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QKeySequenceEdit,
    QPushButton,
    QWidget,
    QLineEdit,
    QComboBox,
    QMessageBox,
    QLayout,
)

from src.core.click_worker import ClickWorkerManager
from src.core.input import InputManager


class PositiveIntValidator(QIntValidator):
    """Filters integer inputs to ensure only positive integers are accepted."""

    @override
    def validate(
        self, input_text: Optional[str], position: int
    ) -> tuple[QIntValidator.State, str, int]:
        """Invalidates using '-' within an integer input field."""
        if input_text is None:
            return QIntValidator.State.Invalid, "", position
        if "-" in input_text:
            return QIntValidator.State.Invalid, input_text, position
        return super().validate(input_text, position)


class HotkeyInput(QKeySequenceEdit):
    """Filters key sequence inputs for hotkeys."""

    @override
    def keyPressEvent(self, key_event: Optional[QKeyEvent]) -> None:
        """
        Filters out non-hotkey keys and performs actions for specific keys:
            - Only allows Ctrl, Shift, Alt, and Meta as hotkey modifiers.
            - Only allows 1 non-modifier key to be used at the end of the hotkey.
            - Enter/Return will unfocus the field.
            - Escape will unfocus the field and clear its value.
        """
        if key_event is None or key_event.isAutoRepeat():
            return

        modifiers = key_event.modifiers()
        key = key_event.key()

        if key in [Qt.Key.Key_Enter, Qt.Key.Key_Return]:
            self.clearFocus()
            return

        if key == Qt.Key.Key_Escape:
            self.clearFocus()
            self.clear()
            return

        modifier_keys = [
            Qt.Key.Key_Control,
            Qt.Key.Key_Shift,
            Qt.Key.Key_Alt,
            Qt.Key.Key_Meta,
        ]

        if key in modifier_keys:
            super().keyPressEvent(key_event)
            return

        modifier_flags = [
            Qt.KeyboardModifier.ControlModifier,
            Qt.KeyboardModifier.ShiftModifier,
            Qt.KeyboardModifier.AltModifier,
            Qt.KeyboardModifier.MetaModifier,
        ]

        has_modifier = any(modifiers & flag for flag in modifier_flags)

        if has_modifier and key not in modifier_keys:
            super().keyPressEvent(key_event)
            return

        key_event.ignore()

    @classmethod
    def from_key_sequence_edit(
        cls, key_sequence_edit: QKeySequenceEdit
    ) -> "HotkeyInput":
        """
        Returns a HotkeyInput based on an existing KeySequenceEdit
        then deletes and replaces the original KeySequenceEdit.
        """

        parent_widget: Optional[QWidget] = key_sequence_edit.parentWidget()
        assert parent_widget is not None

        hotkey_input: HotkeyInput = HotkeyInput(parent_widget)
        hotkey_input.setObjectName(key_sequence_edit.objectName())
        hotkey_input.setGeometry(key_sequence_edit.geometry())
        hotkey_input.setKeySequence(key_sequence_edit.keySequence())

        parent_layout: Optional[QLayout] = parent_widget.layout()
        assert parent_layout is not None

        parent_layout.replaceWidget(key_sequence_edit, hotkey_input)

        key_sequence_edit.deleteLater()
        return hotkey_input


class Window(QMainWindow):
    """The PyQt window implementation for Clikr."""

    def __init__(self) -> None:
        super().__init__()

        self._load_ui()
        self._set_icon()

        self.start_button = self.findChild(QPushButton, "start_button")
        self.stop_button = self.findChild(QPushButton, "stop_button")
        self.tab_widget = self.findChild(QTabWidget, "tab_widget")
        self.simple_tab = self.findChild(QWidget, "simple_tab")
        self.advanced_tab = self.findChild(QWidget, "advanced_tab")
        self.simple_tab_index = self.tab_widget.indexOf(self.simple_tab)
        self.advanced_tab_index = self.tab_widget.indexOf(self.advanced_tab)
        self.simple_hotkey_input = HotkeyInput.from_key_sequence_edit(
            self.findChild(QKeySequenceEdit, "simple_hotkey_input")
        )
        self.simple_location_x_input = self.findChild(
            QLineEdit, "simple_location_x_input"
        )
        self.simple_location_y_input = self.findChild(
            QLineEdit, "simple_location_y_input"
        )
        self.simple_change_location_button = self.findChild(
            QPushButton, "simple_change_location_button"
        )
        self.advanced_hotkey_input = HotkeyInput.from_key_sequence_edit(
            self.findChild(QKeySequenceEdit, "advanced_hotkey_input")
        )
        self.advanced_location_x_input = self.findChild(
            QLineEdit, "advanced_location_x_input"
        )
        self.advanced_location_y_input = self.findChild(
            QLineEdit, "advanced_location_y_input"
        )
        self.advanced_change_location_button = self.findChild(
            QPushButton, "advanced_change_location_button"
        )
        self.simple_interval_input = self.findChild(QLineEdit, "simple_interval_input")
        self.simple_interval_scale_input = self.findChild(
            QComboBox, "simple_interval_scale_input"
        )
        self.simple_mouse_button_input = self.findChild(
            QComboBox, "simple_mouse_button_input"
        )
        self.advanced_interval_input = self.findChild(
            QLineEdit, "advanced_interval_input"
        )
        self.advanced_interval_scale_input = self.findChild(
            QComboBox, "advanced_interval_scale_input"
        )
        self.advanced_hold_length_input = self.findChild(
            QLineEdit, "advanced_hold_length_input"
        )
        self.advanced_hold_length_scale_input = self.findChild(
            QComboBox, "advanced_hold_length_scale_input"
        )
        self.advanced_clicks_per_event_input = self.findChild(
            QLineEdit, "advanced_clicks_per_event_input"
        )
        self.advanced_event_count_input = self.findChild(
            QLineEdit, "advanced_event_count_input"
        )
        self.advanced_mouse_button_input = self.findChild(
            QComboBox, "advanced_mouse_button_input"
        )
        self.__softlock_message_box: Optional[QMessageBox] = None
        self._define_softlock_message_box()

        self._set_validators()

        self._connect_callbacks()

        self.__input_manager = InputManager(
            self.change_location_fields,
            self.change_location_button,
            self.start_stop_toggle,
        )
        self.__click_worker_manager = ClickWorkerManager(self.stop_button.click)

        self.setFixedSize(370, 300)
        self.show()

        logging.debug("Successfully loaded UI")

    @property
    def viewing_advanced_tab(self) -> bool:
        """Returns whether the advanced tab is the tab currently being viewed."""
        return self.tab_widget.currentIndex() == self.advanced_tab_index

    def change_location_button(self) -> QPushButton:
        """Returns the current change location button."""
        if self.viewing_advanced_tab:
            return self.advanced_change_location_button
        return self.simple_change_location_button

    def change_location_fields(self, x: int, y: int) -> None:
        """Sets the location field's X and Y components based on the provided values."""
        if self.viewing_advanced_tab:
            self.advanced_location_x_input.clearFocus()
            self.advanced_location_y_input.clearFocus()
            self.advanced_location_x_input.setText(str(x))
            self.advanced_location_y_input.setText(str(y))
            self.advanced_location_x_input.textEdited.emit(str(x))
            self.advanced_location_y_input.textEdited.emit(str(y))
            return
        self.simple_location_x_input.clearFocus()
        self.simple_location_y_input.clearFocus()
        self.simple_location_x_input.setText(str(x))
        self.simple_location_y_input.setText(str(y))
        self.simple_location_x_input.textEdited.emit(str(x))
        self.simple_location_y_input.textEdited.emit(str(y))

    def _load_ui(self) -> None:
        """Loads the UI layout from the .ui file in the assets directory."""
        source_ui_path = (
            Path(os.path.dirname(__file__))
            .parent.parent.joinpath("assets")
            .joinpath("window.ui")
        )

        if source_ui_path.exists():
            uic.loadUi(str(source_ui_path), self)
            return

        bundled_ui_path = (
            Path(os.path.dirname(__file__)).joinpath("assets").joinpath("window.ui")
        )

        if bundled_ui_path.exists():
            uic.loadUi(str(bundled_ui_path), self)

    def _set_icon(self) -> None:
        """Sets window icon with the icon PNG in the assets directory if the platform is Windows."""
        if not sys.platform.startswith("win"):
            return

        source_icon_path = (
            Path(os.path.dirname(__file__))
            .parent.parent.joinpath("assets")
            .joinpath("icon.png")
        )

        if source_icon_path.exists():
            self.setWindowIcon(QIcon(str(source_icon_path)))
            return

        bundled_icon_path = (
            Path(os.path.dirname(__file__)).joinpath("assets").joinpath("icon.png")
        )

        if bundled_icon_path.exists():
            self.setWindowIcon(QIcon(str(bundled_icon_path)))

    def _define_softlock_message_box(self) -> None:
        """Defines the content of the softlock prevention pop-up."""
        self.__softlock_message_box = QMessageBox(self)
        self.__softlock_message_box.setIcon(QMessageBox.Icon.Warning)
        self.__softlock_message_box.setWindowTitle("Softlock Prevention")
        self.__softlock_message_box.setText(
            "You must set a hotkey if you are using a location.\n"
            "This prevents you from softlocking your mouse."
        )
        self.__softlock_message_box.setStandardButtons(QMessageBox.StandardButton.Ok)

    def _set_validators(self) -> None:
        """Sets the validator to the PositiveIntValidator for each QLineEdit."""
        for line_edit in self.findChildren(QLineEdit):
            line_edit.setValidator(PositiveIntValidator())

    def _connect_callbacks(self) -> None:
        """Connects each UI signal to its corresponding handler."""
        self.tab_widget.currentChanged.connect(self._on_tab_changed)

        self.simple_interval_input.textEdited.connect(self._update_unscaled_interval)
        self.simple_interval_scale_input.currentIndexChanged.connect(
            self._update_interval_timescale
        )
        self.simple_location_x_input.textEdited.connect(self._update_location_x)
        self.simple_location_y_input.textEdited.connect(self._update_location_y)
        self.simple_change_location_button.clicked.connect(
            self._on_change_location_button_clicked
        )
        self.simple_hotkey_input.keySequenceChanged.connect(self._update_hotkey)

        self.advanced_interval_input.textEdited.connect(self._update_unscaled_interval)
        self.advanced_interval_scale_input.currentIndexChanged.connect(
            self._update_interval_timescale
        )
        self.advanced_hold_length_input.textEdited.connect(
            self._update_unscaled_hold_length
        )
        self.advanced_hold_length_scale_input.currentIndexChanged.connect(
            self._update_hold_length_timescale
        )
        self.advanced_clicks_per_event_input.textEdited.connect(
            self._update_clicks_per_event
        )
        self.advanced_event_count_input.textEdited.connect(self._update_event_count)
        self.advanced_location_x_input.textEdited.connect(self._update_location_x)
        self.advanced_location_y_input.textEdited.connect(self._update_location_y)
        self.advanced_change_location_button.clicked.connect(
            self._on_change_location_button_clicked
        )
        self.advanced_hotkey_input.keySequenceChanged.connect(self._update_hotkey)

        self.start_button.clicked.connect(self._on_start_button_clicked)
        self.stop_button.clicked.connect(self._on_stop_button_clicked)

        for line_edit in self.findChildren(QLineEdit):
            line_edit.returnPressed.connect(line_edit.clearFocus)

    def _update_unscaled_interval(self) -> None:
        """Updates the input manager with the field's current unscaled interval."""
        if self.viewing_advanced_tab:
            self.__input_manager.update_unscaled_interval(self.advanced_interval_input)
            return
        self.__input_manager.update_unscaled_interval(self.simple_interval_input)

    def _update_interval_timescale(self) -> None:
        """Updates the input manager with the field's current interval timescale."""
        if self.viewing_advanced_tab:
            self.__input_manager.update_interval_timescale(
                self.advanced_interval_scale_input
            )
            return
        self.__input_manager.update_interval_timescale(self.simple_interval_scale_input)

    def _update_unscaled_hold_length(self) -> None:
        """Updates the input manager with the field's current unscaled hold length."""
        self.__input_manager.update_unscaled_hold_length(
            self.advanced_hold_length_input
        )

    def _update_hold_length_timescale(self) -> None:
        """Updates the input manager with the field's current hold length timescale."""
        self.__input_manager.update_hold_length_timescale(
            self.advanced_hold_length_scale_input
        )

    def _update_clicks_per_event(self) -> None:
        """Updates the input manager with the field's current clicks per event."""
        self.__input_manager.update_clicks_per_event(
            self.advanced_clicks_per_event_input
        )

    def _update_event_count(self) -> None:
        """Updates the input manager with the field's current event count."""
        self.__input_manager.update_event_count(self.advanced_event_count_input)

    def _update_location_x(self) -> None:
        """Updates the input manager with the field's current location X component."""
        if self.viewing_advanced_tab:
            self.__input_manager.update_location_x(self.advanced_location_x_input)
            return
        self.__input_manager.update_location_x(self.simple_location_x_input)

    def _update_location_y(self) -> None:
        """Updates the input manager with the field's current location Y component."""
        if self.viewing_advanced_tab:
            self.__input_manager.update_location_y(self.advanced_location_y_input)
            return
        self.__input_manager.update_location_y(self.simple_location_y_input)

    def _update_hotkey(self) -> None:
        """Updates the input manager with the field's current hotkey."""
        if self.viewing_advanced_tab:
            self.__input_manager.update_hotkey(self.advanced_hotkey_input)
            return
        self.__input_manager.update_hotkey(self.simple_hotkey_input)

    def _update_inputs(self) -> None:
        """Updates the input manager with of the current field values."""
        self._update_unscaled_interval()
        self._update_interval_timescale()
        self._update_unscaled_hold_length()
        self._update_hold_length_timescale()
        self._update_clicks_per_event()
        self._update_event_count()
        self._update_location_x()
        self._update_location_y()
        self._update_hotkey()

    def _on_change_location_button_clicked(self) -> None:
        """Starts the input manager's listeners to change the location."""
        self.__input_manager.listen_for_location()

    def _on_start_button_clicked(self) -> None:
        """
        Checks if the softlock prevention message should pop up,
        otherwise toggles the start/stop buttons and starts the click worker.
        """
        if self.__input_manager.can_softlock:
            assert self.__softlock_message_box is not None
            logging.debug("Displaying softlock prevention message")
            self.__softlock_message_box.exec()
            return
        self.stop_button.setDisabled(False)
        self.start_button.setDisabled(True)
        self.__click_worker_manager.start(self.__input_manager.worker_inputs)

    def _on_stop_button_clicked(self) -> None:
        """Toggles the start/stop buttons and stops the click worker."""
        self.stop_button.setDisabled(True)
        self.start_button.setDisabled(False)
        self.__click_worker_manager.stop()

    def start_stop_toggle(self) -> None:
        """Toggles the start/stop buttons."""
        if self.stop_button.isEnabled():
            logging.debug("Clicking stop button")
            self.stop_button.click()
            return
        logging.debug("Clicking start button")
        self.start_button.click()

    def _on_tab_changed(self) -> None:
        """
        Stops the click worker and updates
        the input manager for the new tab's input fields.
        """
        self.__click_worker_manager.stop()
        self._update_inputs()
