import logging
import os
import sys
from pathlib import Path
from typing import Optional, Self

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
)

from src.core.click_worker import ClickWorkerManager
from src.core.input import InputManager


class PositiveIntValidator(QIntValidator):
    def validate(self, input_text: str, pos: int) -> tuple:
        if "-" in input_text:
            return QIntValidator.State.Invalid, input_text, pos
        return super().validate(input_text, pos)


class HotkeyInput(QKeySequenceEdit):

    def __init__(self, widget):
        super().__init__(widget)

    def keyPressEvent(self, event: QKeyEvent):
        if event.isAutoRepeat():
            return

        modifiers = event.modifiers()
        key = event.key()

        if key in [Qt.Key.Key_Enter, Qt.Key.Key_Return]:
            self.clearFocus()
            return

        if key == Qt.Key.Key_Escape:
            self.clear()
            self.clearFocus()
            return

        modifier_keys = [
            Qt.Key.Key_Control,
            Qt.Key.Key_Shift,
            Qt.Key.Key_Alt,
            Qt.Key.Key_Meta,
        ]

        if key in modifier_keys:
            super().keyPressEvent(event)
            return

        modifier_flags = [
            Qt.KeyboardModifier.ControlModifier,
            Qt.KeyboardModifier.ShiftModifier,
            Qt.KeyboardModifier.AltModifier,
            Qt.KeyboardModifier.MetaModifier,
        ]

        has_modifier = any(modifiers & flag for flag in modifier_flags)

        if has_modifier and key not in modifier_keys:
            super().keyPressEvent(event)
            return

        event.ignore()

    @classmethod
    def from_key_sequence_edit(cls, key_sequence_edit: QKeySequenceEdit) -> Self:
        hotkey_input = HotkeyInput(key_sequence_edit.parent())
        hotkey_input.setObjectName(key_sequence_edit.objectName())
        hotkey_input.setGeometry(key_sequence_edit.geometry())
        hotkey_input.setKeySequence(key_sequence_edit.keySequence())

        if key_sequence_edit.parent().layout():
            layout = key_sequence_edit.parent().layout()
            layout.replaceWidget(key_sequence_edit, hotkey_input)

        key_sequence_edit.deleteLater()
        return hotkey_input


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.__load_ui()
        self.__set_icon()

        self.__start_button = self.findChild(QPushButton, "start_button")
        self.__stop_button = self.findChild(QPushButton, "stop_button")
        self.__tab_widget = self.findChild(QTabWidget, "tab_widget")
        self.__simple_tab = self.findChild(QWidget, "simple_tab")
        self.__advanced_tab = self.findChild(QWidget, "advanced_tab")
        self.__simple_tab_index = self.__tab_widget.indexOf(self.__simple_tab)
        self.__advanced_tab_index = self.__tab_widget.indexOf(self.__advanced_tab)
        self.__simple_hotkey_input = HotkeyInput.from_key_sequence_edit(
            self.findChild(QKeySequenceEdit, "simple_hotkey_input")
        )
        self.__simple_location_x_input = self.findChild(
            QLineEdit, "simple_location_x_input"
        )
        self.__simple_location_y_input = self.findChild(
            QLineEdit, "simple_location_y_input"
        )
        self.__simple_change_location_button = self.findChild(
            QPushButton, "simple_change_location_button"
        )
        self.__advanced_hotkey_input = HotkeyInput.from_key_sequence_edit(
            self.findChild(QKeySequenceEdit, "advanced_hotkey_input")
        )
        self.__advanced_location_x_input = self.findChild(
            QLineEdit, "advanced_location_x_input"
        )
        self.__advanced_location_y_input = self.findChild(
            QLineEdit, "advanced_location_y_input"
        )
        self.__advanced_change_location_button = self.findChild(
            QPushButton, "advanced_change_location_button"
        )
        self.__simple_interval_input = self.findChild(
            QLineEdit, "simple_interval_input"
        )
        self.__simple_interval_scale_input = self.findChild(
            QComboBox, "simple_interval_scale_input"
        )
        self.__simple_mouse_button_input = self.findChild(
            QComboBox, "simple_mouse_button_input"
        )
        self.__advanced_interval_input = self.findChild(
            QLineEdit, "advanced_interval_input"
        )
        self.__advanced_interval_scale_input = self.findChild(
            QComboBox, "advanced_interval_scale_input"
        )
        self.__advanced_hold_length_input = self.findChild(
            QLineEdit, "advanced_hold_length_input"
        )
        self.__advanced_hold_length_scale_input = self.findChild(
            QComboBox, "advanced_hold_length_scale_input"
        )
        self.__advanced_clicks_per_event_input = self.findChild(
            QLineEdit, "advanced_clicks_per_event_input"
        )
        self.__advanced_event_count_input = self.findChild(
            QLineEdit, "advanced_event_count_input"
        )
        self.__advanced_mouse_button_input = self.findChild(
            QComboBox, "advanced_mouse_button_input"
        )
        self.__softlock_message_box: Optional[QMessageBox] = None
        self.__define_softlock_message_box()

        self.__initialize_validators()
        self.__connect_callbacks()

        self.__input_manager = InputManager(
            self.__change_location_fields,
            self.__change_location_button,
            self.start_stop_toggle,
        )

        self.__click_worker_manager = ClickWorkerManager(
            finished_callback=self.__stop_button.click
        )

        self.setFixedSize(370, 300)
        self.show()

        logging.debug("Successfully loaded UI")

    def __load_ui(self):
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

    def __set_icon(self):
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

    def __define_softlock_message_box(self):
        self.__softlock_message_box = QMessageBox(self)
        self.__softlock_message_box.setIcon(QMessageBox.Icon.Warning)
        self.__softlock_message_box.setWindowTitle("Softlock Prevention")
        self.__softlock_message_box.setText(
            "You must set a hotkey if you are using a location.\n"
            "This prevents you from softlocking your mouse."
        )
        self.__softlock_message_box.setStandardButtons(QMessageBox.StandardButton.Ok)

    def __initialize_validators(self):
        self.__simple_interval_input.setValidator(PositiveIntValidator())
        self.__simple_location_x_input.setValidator(PositiveIntValidator())
        self.__simple_location_y_input.setValidator(PositiveIntValidator())
        self.__advanced_interval_input.setValidator(PositiveIntValidator())
        self.__advanced_hold_length_input.setValidator(PositiveIntValidator())
        self.__advanced_clicks_per_event_input.setValidator(PositiveIntValidator())
        self.__advanced_event_count_input.setValidator(PositiveIntValidator())
        self.__advanced_location_x_input.setValidator(PositiveIntValidator())
        self.__advanced_location_y_input.setValidator(PositiveIntValidator())

    def __connect_callbacks(self):
        self.__tab_widget.currentChanged.connect(self.__on_tab_changed)

        self.__simple_interval_input.textEdited.connect(self.__update_interval)
        self.__simple_interval_scale_input.currentIndexChanged.connect(
            self.__update_interval_timescale
        )
        self.__simple_location_x_input.textEdited.connect(self.__update_location_x)
        self.__simple_location_y_input.textEdited.connect(self.__update_location_y)
        self.__simple_change_location_button.clicked.connect(
            self.__on_change_location_button_clicked
        )
        self.__simple_hotkey_input.keySequenceChanged.connect(self.__update_hotkey)

        self.__advanced_interval_input.textEdited.connect(self.__update_interval)
        self.__advanced_interval_scale_input.currentIndexChanged.connect(
            self.__update_interval_timescale
        )
        self.__advanced_hold_length_input.textEdited.connect(self.__update_hold_length)
        self.__advanced_hold_length_scale_input.currentIndexChanged.connect(
            self.__update_hold_length_timescale
        )
        self.__advanced_clicks_per_event_input.textEdited.connect(
            self.__update_clicks_per_event
        )
        self.__advanced_event_count_input.textEdited.connect(self.__update_event_count)
        self.__advanced_location_x_input.textEdited.connect(self.__update_location_x)
        self.__advanced_location_y_input.textEdited.connect(self.__update_location_y)
        self.__advanced_change_location_button.clicked.connect(
            self.__on_change_location_button_clicked
        )
        self.__advanced_hotkey_input.keySequenceChanged.connect(self.__update_hotkey)

        self.__start_button.clicked.connect(self.__on_start_button_clicked)
        self.__stop_button.clicked.connect(self.__on_stop_button_clicked)

        for line_edit in self.findChildren(QLineEdit):
            line_edit.returnPressed.connect(line_edit.clearFocus)

    def __update_interval(self):
        if self.__viewing_advanced_tab:
            self.__input_manager.interval_seconds = self.__advanced_interval_input
            return
        self.__input_manager.interval_seconds = self.__simple_interval_input

    def __update_interval_timescale(self):
        if self.__viewing_advanced_tab:
            self.__input_manager.interval_timescale = (
                self.__advanced_interval_scale_input
            )
            return
        self.__input_manager.interval_timescale = self.__simple_interval_scale_input

    def __update_hold_length(self):
        self.__input_manager.hold_length_seconds = self.__advanced_hold_length_input

    def __update_hold_length_timescale(self):
        self.__input_manager.hold_length_timescale = (
            self.__advanced_hold_length_scale_input
        )

    def __update_clicks_per_event(self):
        self.__input_manager.clicks_per_event = self.__advanced_clicks_per_event_input

    def __update_event_count(self):
        self.__input_manager.event_count = self.__advanced_event_count_input

    def __update_location_x(self):
        if self.__viewing_advanced_tab:
            self.__input_manager.location_x = self.__advanced_location_x_input
            return
        self.__input_manager.location_x = self.__simple_location_x_input

    def __update_location_y(self):
        if self.__viewing_advanced_tab:
            self.__input_manager.location_y = self.__advanced_location_y_input
            return
        self.__input_manager.location_y = self.__simple_location_y_input

    def __update_hotkey(self):
        if self.__viewing_advanced_tab:
            self.__input_manager.hotkey = self.__advanced_hotkey_input
            return
        self.__input_manager.hotkey = self.__simple_hotkey_input

    def __update_inputs(self):
        self.__update_interval()
        self.__update_interval_timescale()
        self.__update_hold_length()
        self.__update_hold_length_timescale()
        self.__update_clicks_per_event()
        self.__update_event_count()
        self.__update_location_x()
        self.__update_location_y()
        self.__update_hotkey()

    def __change_location_fields(self, x: int, y: int):
        if self.__viewing_advanced_tab:
            self.__advanced_location_x_input.setText(str(x))
            self.__advanced_location_x_input.textEdited.emit(str(x))
            self.__advanced_location_x_input.clearFocus()
            self.__advanced_location_y_input.setText(str(y))
            self.__advanced_location_y_input.textEdited.emit(str(y))
            self.__advanced_location_y_input.clearFocus()
            return
        self.__simple_location_x_input.setText(str(x))
        self.__simple_location_x_input.textEdited.emit(str(x))
        self.__simple_location_x_input.clearFocus()
        self.__simple_location_y_input.setText(str(y))
        self.__simple_location_y_input.textEdited.emit(str(y))
        self.__simple_location_y_input.clearFocus()

    def __change_location_button(self) -> QPushButton:
        if self.__viewing_advanced_tab:
            return self.__advanced_change_location_button
        return self.__simple_change_location_button

    @property
    def __viewing_advanced_tab(self):
        return self.__tab_widget.currentIndex() == self.__advanced_tab_index

    def __on_change_location_button_clicked(self):
        self.__input_manager.change_location()

    def __on_start_button_clicked(self):
        if self.__input_manager.can_softlock:
            logging.info("Displaying softlock prevention message")
            self.__softlock_message_box.exec()
            return
        self.__stop_button.setDisabled(False)
        self.__start_button.setDisabled(True)
        self.__click_worker_manager.start(self.__input_manager.worker_inputs)

    def __on_stop_button_clicked(self):
        self.__stop_button.setDisabled(True)
        self.__start_button.setDisabled(False)
        self.__click_worker_manager.stop()

    def start_stop_toggle(self):
        if self.__stop_button.isEnabled():
            logging.debug("Clicking stop button")
            self.__stop_button.click()
            return
        logging.debug("Clicking start button")
        self.__start_button.click()

    def __on_tab_changed(self):
        self.__click_worker_manager.stop()
        self.__update_inputs()
