import logging
import os
import sys
from pathlib import Path
from time import sleep
from typing import Optional, Self

from PyQt6 import uic
from PyQt6.QtCore import pyqtSlot, QThread, pyqtSignal, Qt
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
from pynput import keyboard, mouse

from click_worker import WorkerInputs, ClickWorker


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

    worker_requested = pyqtSignal()
    change_inputs = pyqtSignal(WorkerInputs)

    def __init__(self):
        super().__init__()
        self.current_hotkey = None
        self.advanced_location = None
        self.simple_location = None
        self.esc_key_listener = None
        self.hotkey_listener = None
        self.location_click_listener = None
        self.first_tab_switch = True
        self.mouse_controller = mouse.Controller()

        self.load_ui()
        self.set_icon()

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
        self.simple_location_display = self.findChild(
            QLineEdit, "simple_location_display"
        )
        self.simple_change_location_button = self.findChild(
            QPushButton, "simple_change_location_button"
        )
        self.advanced_hotkey_input = HotkeyInput.from_key_sequence_edit(
            self.findChild(QKeySequenceEdit, "advanced_hotkey_input")
        )
        self.advanced_location_display = self.findChild(
            QLineEdit, "advanced_location_display"
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
        self.softlock_message_box: Optional[QMessageBox] = None
        self.define_message_box()

        self.initialize_validators()
        self.connect_callbacks()

        self.click_worker = ClickWorker
        self.worker_thread = QThread
        self.initialize_click_worker()

        self.adjustSize()
        self.show()

    def load_ui(self):
        source_ui_path = (
            Path(os.path.dirname(__file__))
            .parent.joinpath("assets")
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
            return

    def set_icon(self):
        if not sys.platform.startswith("win"):
            return

        source_icon_path = (
            Path(os.path.dirname(__file__))
            .parent.joinpath("assets")
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
            return

    def define_message_box(self):
        self.softlock_message_box = QMessageBox(self)
        self.softlock_message_box.setIcon(QMessageBox.Icon.Warning)
        self.softlock_message_box.setWindowTitle("Softlock Prevention")
        self.softlock_message_box.setText(
            "You must set a hotkey if you are using a location.\n"
            "This prevents you from softlocking your mouse."
        )
        self.softlock_message_box.setStandardButtons(QMessageBox.StandardButton.Ok)

    def initialize_click_worker(self):
        self.click_worker = ClickWorker(self.inputs, self.mouse_controller)
        self.worker_thread = QThread()
        self.click_worker.finished.connect(self.stop_button_clicked)
        self.change_inputs.connect(self.click_worker.change_inputs)
        self.worker_requested.connect(self.click_worker.start)
        self.click_worker.moveToThread(self.worker_thread)

    @staticmethod
    def connect_return_clear_focus(line_edit: QLineEdit):
        line_edit.returnPressed.connect(line_edit.clearFocus)

    def connect_callbacks(self):
        self.tab_widget.currentChanged.connect(self.switched_tabs)
        self.simple_hotkey_input.editingFinished.connect(self.hotkey_changed)
        self.simple_hotkey_input.clear_callback = lambda: setattr(
            self, "simple_location", None
        )
        self.simple_hotkey_input.keySequenceChanged.connect(self.stop_hotkey_listener)
        self.simple_change_location_button.pressed.connect(self.change_location)
        self.advanced_hotkey_input.editingFinished.connect(self.hotkey_changed)
        self.advanced_hotkey_input.keySequenceChanged.connect(self.stop_hotkey_listener)
        self.advanced_hotkey_input.clear_callback = lambda: setattr(
            self, "advanced_location", None
        )
        self.advanced_change_location_button.pressed.connect(self.change_location)
        self.start_button.clicked.connect(self.start_button_clicked)
        self.stop_button.clicked.connect(self.stop_button_clicked)
        self.connect_return_clear_focus(self.simple_interval_input)
        self.connect_return_clear_focus(self.advanced_interval_input)
        self.connect_return_clear_focus(self.advanced_hold_length_input)
        self.connect_return_clear_focus(self.advanced_event_count_input)
        self.connect_return_clear_focus(self.advanced_clicks_per_event_input)

    def initialize_validators(self):
        self.simple_interval_input.setValidator(PositiveIntValidator())
        self.advanced_interval_input.setValidator(PositiveIntValidator())
        self.advanced_hold_length_input.setValidator(PositiveIntValidator())
        self.advanced_clicks_per_event_input.setValidator(PositiveIntValidator())
        self.advanced_event_count_input.setValidator(PositiveIntValidator())

    @property
    def viewing_advanced_tab(self):
        return self.tab_widget.currentIndex() == self.advanced_tab_index

    @property
    def inputs(self) -> WorkerInputs:
        inputs = WorkerInputs()
        if self.viewing_advanced_tab:
            if self.advanced_interval_input.text() != "":
                inputs.interval = int(self.advanced_interval_input.text())
            inputs.interval_scale_index = (
                self.advanced_interval_scale_input.currentIndex()
            )
            if self.advanced_hold_length_input.text() != "":
                inputs.hold_length = int(self.advanced_hold_length_input.text())
            inputs.hold_length_scale_index = (
                self.advanced_hold_length_scale_input.currentIndex()
            )
            if self.advanced_clicks_per_event_input.text() != "":
                inputs.clicks_per_event = int(
                    self.advanced_clicks_per_event_input.text()
                )
            inputs.event_count = (
                int(self.advanced_event_count_input.text())
                if self.advanced_event_count_input.text() != ""
                else None
            )
            inputs.location = self.advanced_location
            inputs.mouse_button_index = self.advanced_mouse_button_input.currentIndex()
        else:
            if self.simple_interval_input.text() != "":
                inputs.interval = int(self.simple_interval_input.text())
            inputs.interval_scale_index = (
                self.simple_interval_scale_input.currentIndex()
            )
            inputs.location = self.simple_location
            inputs.mouse_button_index = self.simple_mouse_button_input.currentIndex()
        return inputs

    @property
    def softlock_capable(self) -> bool:
        return (
            not self.viewing_advanced_tab
            and self.simple_location is not None
            and self.simple_hotkey_input.keySequence().isEmpty()
        ) or (
            self.viewing_advanced_tab
            and self.advanced_location is not None
            and self.advanced_event_count_input.text() == ""
            and self.advanced_hotkey_input.keySequence().isEmpty()
        )

    def pynput_key_sequence(self, key_sequence: str) -> str:
        bracketed_keys = {
            "f1",
            "f2",
            "f3",
            "f4",
            "f5",
            "f6",
            "f7",
            "f8",
            "f9",
            "f10",
            "f11",
            "f12",
            "ctrl",
            "shift",
            "alt",
            "meta",
            "cmd",
            "space",
        }

        pynput_key_sequence = key_sequence.replace(" ", "").lower()
        parts = pynput_key_sequence.split("+")

        converted_parts = [
            f"<{part}>" if part in bracketed_keys and not part.startswith("<") else part
            for part in parts
        ]

        pynput_key_sequence = "+".join(converted_parts)
        logging.info(f"Converting pyqt {key_sequence} to pynput {pynput_key_sequence}")
        return pynput_key_sequence

    def clear_hotkey_focus(self):
        (
            self.advanced_hotkey_input.clearFocus()
            if self.viewing_advanced_tab
            else self.simple_hotkey_input.clearFocus()
        )

    def add_hotkey(self, key_sequence: str, callback) -> Optional[str]:
        def for_canonical(f):
            return lambda k: f(listener.canonical(k))

        def on_activate():
            callback()

        try:
            hotkey = keyboard.HotKey(keyboard.HotKey.parse(key_sequence), on_activate)

            listener = keyboard.Listener(
                on_press=for_canonical(hotkey.press),
                on_release=for_canonical(hotkey.release),
            )
            listener.start()
            self.hotkey_listener = listener
            self.clear_hotkey_focus()
            return key_sequence
        except ValueError as value:
            logging.error(f"Failed to set hotkey: {value}")
            self.clear_hotkey_focus()
            return None

    def on_location_click(self, callback):
        def click_handler(x, y, button, pressed):
            if pressed:
                callback()

        self.location_click_listener = mouse.Listener(on_click=click_handler)
        self.location_click_listener.start()

    def on_press_esc(self, callback):
        def key_handler(key):
            if key == keyboard.Key.esc:
                callback()

        self.esc_key_listener = keyboard.Listener(on_press=key_handler)
        self.esc_key_listener.start()

    def stop_location_click_listener(self):
        if self.location_click_listener:
            self.location_click_listener.stop()
            try:
                self.location_click_listener.join()
            except RuntimeError:
                pass
            self.location_click_listener = None

    def stop_esc_key_listener(self):
        if self.esc_key_listener:
            self.esc_key_listener.stop()
            try:
                self.esc_key_listener.join()
            except RuntimeError:
                pass
            self.esc_key_listener = None

    def stop_hotkey_listener(self):
        if self.current_hotkey:
            self.current_hotkey = None
        if self.hotkey_listener:
            self.hotkey_listener.stop()
            try:
                self.hotkey_listener.join()
            except RuntimeError:
                pass
            self.hotkey_listener = None

    def stop_click_worker(self):
        if self.worker_thread.isRunning():
            logging.info("Terminating worker thread")
            self.worker_thread.terminate()
            self.worker_thread.wait()

    @pyqtSlot()
    def start_button_clicked(self):
        if self.softlock_capable:
            logging.info("Displaying softlock prevention message")
            self.softlock_message_box.exec()
            return
        self.stop_button.setDisabled(False)
        self.start_button.setDisabled(True)
        self.change_inputs.emit(self.inputs)
        self.worker_thread.start()
        self.worker_requested.emit()

    @pyqtSlot()
    def stop_button_clicked(self):
        self.stop_button.setDisabled(True)
        self.start_button.setDisabled(False)
        self.stop_click_worker()

    @pyqtSlot()
    def switched_tabs(self):
        if self.first_tab_switch:
            self.first_tab_switch = False
            return
        self.stop_click_worker()

    @pyqtSlot()
    def hotkey_changed(self):
        sender = self.sender()
        (
            self.simple_hotkey_input.setKeySequence(
                self.advanced_hotkey_input.keySequence()
            )
            if sender == self.advanced_hotkey_input
            else self.advanced_hotkey_input.setKeySequence(
                self.simple_hotkey_input.keySequence()
            )
        )
        key_sequence = sender.keySequence().toString()
        if key_sequence:
            self.stop_hotkey_listener()
            self.current_hotkey = self.add_hotkey(
                self.pynput_key_sequence(key_sequence), self.hotkey_toggle
            )
        logging.info(f"Hotkey set to {self.current_hotkey}")

    def hotkey_toggle(self):
        (
            self.stop_button_clicked()
            if self.worker_thread.isRunning()
            else self.start_button_clicked()
        )

    def clear_location_and_listener(self):
        logging.info("Clearing location value")
        self.stop_location_click_listener()
        self.stop_esc_key_listener()
        if self.viewing_advanced_tab:
            self.advanced_location_display.clear()
            self.advanced_location = None
            self.advanced_change_location_button.setEnabled(True)
        else:
            self.simple_location_display.clear()
            self.simple_location = None
            self.simple_change_location_button.setEnabled(True)

    def change_location(self):
        advanced_tab = self.viewing_advanced_tab

        def set_location():
            x, y = self.mouse_controller.position
            if advanced_tab:
                self.advanced_location = (x, y)
                self.advanced_change_location_button.setEnabled(True)
                logging.info(f"Set advanced location to {self.advanced_location}")
            else:
                self.simple_location = (x, y)
                self.simple_change_location_button.setEnabled(True)
                logging.info(f"Set simple location to {self.simple_location}")
            self.update_location_displays()
            self.stop_location_click_listener()
            self.stop_esc_key_listener()

        (
            self.advanced_change_location_button.setEnabled(False)
            if advanced_tab
            else self.simple_change_location_button.setEnabled(False)
        )

        (
            logging.info(
                "Listening for advanced location, waiting for click or esc press"
            )
            if advanced_tab
            else logging.info(
                "Listening for simple location, waiting for click or esc press"
            )
        )

        self.on_press_esc(self.clear_location_and_listener)
        sleep(0.2)
        self.on_location_click(set_location)

    def update_location_displays(self):
        if self.advanced_location is not None:
            self.advanced_location_display.setText(
                f"({self.advanced_location[0]}, {self.advanced_location[1]})"
            )
        if self.simple_location is not None:
            self.simple_location_display.setText(
                f"({self.simple_location[0]}, {self.simple_location[1]})"
            )
