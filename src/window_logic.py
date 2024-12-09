from time import sleep
from typing import Optional

import pyautogui
from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal, QThread

from pynput import keyboard, mouse

from click_process import ClickProcessInputs, ClickProcess, AdvancedClickProcess
from window_init import MainWindow


class FinishedSignalEmitter(QObject):
    finished_signal = pyqtSignal()


class AppWindow(MainWindow):

    def __init__(self, logger):
        super().__init__(logger)
        self.logger = logger
        self._finished_emitter = FinishedSignalEmitter()
        self._finished_emitter.finished_signal.connect(self.stop_button_clicked)
        self._current_click_process = None
        self.keyboard_listener = None
        self.mouse_listener = None

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
        self.logger.info(
            "Converting pyqt %s to pynput %s", key_sequence, pynput_key_sequence
        )
        return pynput_key_sequence

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
            self.keyboard_listener = listener
            return key_sequence
        except ValueError as value:
            self.logger.error(f"Failed to set hotkey: {value}")
            return None

    def on_click(self, callback):
        def click_handler(x, y, button, pressed):
            if pressed:
                callback()

        self.mouse_listener = mouse.Listener(on_click=click_handler)
        self.mouse_listener.start()

    def join_mouse_listener(self):
        if self.mouse_listener:
            self.mouse_listener.stop()
            try:
                self.mouse_listener.join()
            except RuntimeError:
                pass
            self.mouse_listener = None

    def clear_hotkey(self):
        if self.current_hotkey:
            self.current_hotkey = None
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            try:
                self.keyboard_listener.join()
            except RuntimeError:
                pass
            self.keyboard_listener = None

    def clear_hotkey_field(self):
        key_sequence_edit = self.sender()
        if 16777216 in list(key_sequence_edit.keySequence()):
            key_sequence_edit.clearFocus()
            self.smpl_hkey_keyseq.clear()
            self.adv_hkey_keyseq.clear()
        self.clear_hotkey()

    @property
    def in_advanced_tab(self):
        return self.tab_wgt.currentIndex() == 1

    @property
    def inputs(self) -> ClickProcessInputs:
        inputs = ClickProcessInputs()
        inputs.is_advanced = self.in_advanced_tab
        if inputs.is_advanced:
            if self.adv_clk_intvl_ledit.text() != "":
                inputs.click_interval = int(self.adv_clk_intvl_ledit.text())
            inputs.click_interval_scale_index = (
                self.adv_clk_intvl_scale_cbox.currentIndex()
            )
            if self.adv_clen_ledit.text() != "":
                inputs.click_length = int(self.adv_clen_ledit.text())
            inputs.click_length_scale_index = self.adv_clen_scale_cbox.currentIndex()
            if self.adv_clicks_per_event_ledit.text() != "":
                inputs.clicks_per_event = int(self.adv_clicks_per_event_ledit.text())
            inputs.click_events = (
                int(self.adv_clk_events_ledit.text())
                if self.adv_clk_events_ledit.text() != ""
                else None
            )
            inputs.click_location = self.advanced_location
            inputs.mouse_button_index = self.adv_mb_cbox.currentIndex()
        else:
            if self.smpl_clk_intvl_ledit.text() != "":
                inputs.click_interval = int(self.smpl_clk_intvl_ledit.text())
            inputs.click_interval_scale_index = (
                self.smpl_clk_intvl_scale_cbox.currentIndex()
            )
            inputs.click_location = self.simple_location
            inputs.mouse_button_index = self.smpl_mb_cbox.currentIndex()
        return inputs

    @property
    def softlock_capable(self) -> bool:
        return (
            not self.in_advanced_tab
            and self.simple_location is not None
            and self.smpl_hkey_keyseq.keySequence().isEmpty()
        ) or (
            self.in_advanced_tab
            and self.advanced_location is not None
            and self.adv_clk_events_ledit.text() == ""
            and self.adv_hkey_keyseq.keySequence().isEmpty()
        )

    @pyqtSlot()
    def start_button_clicked(self):
        if self.softlock_capable:
            self.logger.info("Displaying softlock prevention message")
            self.softlock_warning_msgb.exec()
            return
        self.active_process = True
        self.stop_btn.setDisabled(False)
        self.start_btn.setDisabled(True)
        ClickProcess.terminate_all(self.logger)
        click_process = ClickProcess.get_appropriate(self.inputs, self.logger)
        if (
            isinstance(click_process, AdvancedClickProcess)
            and click_process.click_events is not None
        ):
            self._start_finished_event_watcher(click_process)
        click_process.start()
        self._current_click_process = click_process

    @pyqtSlot()
    def stop_button_clicked(self):
        self.active_process = False
        self.stop_btn.setDisabled(True)
        self.start_btn.setDisabled(False)
        ClickProcess.terminate_all(self.logger)

    def _start_finished_event_watcher(self, click_process):
        def wait_for_finished():
            click_process.finished.wait()
            self._finished_emitter.finished_signal.emit()

        thread = QThread()
        thread.run = wait_for_finished
        thread.start()

    @pyqtSlot()
    def switched_tabs(self):
        if self.first_tab_switch:
            self.first_tab_switch = False
            return
        ClickProcess.terminate_all(self.logger)

    @pyqtSlot()
    def hotkey_changed(self):
        sender = self.sender()
        (
            self.smpl_hkey_keyseq.setKeySequence(self.adv_hkey_keyseq.keySequence())
            if sender == self.adv_hkey_keyseq
            else self.adv_hkey_keyseq.setKeySequence(
                self.smpl_hkey_keyseq.keySequence()
            )
        )
        key_sequence = sender.keySequence().toString()
        if key_sequence:
            self.clear_hotkey()
            self.current_hotkey = self.add_hotkey(
                self.pynput_key_sequence(key_sequence), self.hotkey_toggle
            )
        self.logger.info("Hotkey set to %s", self.current_hotkey)

    def hotkey_toggle(self):
        (
            self.stop_button_clicked()
            if self.active_process
            else self.start_button_clicked()
        )

    def change_location(self):
        advanced_tab = self.in_advanced_tab

        def set_location():
            x, y = pyautogui.position()
            if advanced_tab:
                self.advanced_location = (x, y)
                self.adv_change_loc_btn.setEnabled(True)
                self.logger.info("Set advanced location to %s", self.advanced_location)
            else:
                self.simple_location = (x, y)
                self.smpl_change_loc_btn.setEnabled(True)
                self.logger.info("Set simple location to %s", self.simple_location)
            self.update_location_displays()
            self.join_mouse_listener()

        (
            self.adv_change_loc_btn.setEnabled(False)
            if advanced_tab
            else self.smpl_change_loc_btn.setEnabled(False)
        )

        (
            self.logger.info(
                "Hooked mouse to set advanced location; waiting for location click"
            )
            if advanced_tab
            else self.logger.info(
                "Hooked mouse to set simple location; waiting for location click"
            )
        )

        sleep(0.2)
        self.on_click(set_location)

    def update_location_displays(self):
        if self.advanced_location is not None:
            self.adv_loc_display_ledit.setText(
                f"({self.advanced_location[0]}, {self.advanced_location[1]})"
            )
        if self.simple_location is not None:
            self.smpl_loc_display_ledit.setText(
                f"({self.simple_location[0]}, {self.simple_location[1]})"
            )
