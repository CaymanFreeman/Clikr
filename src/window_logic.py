from time import sleep
from typing import Optional

from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread

from pynput import keyboard, mouse

from click_worker import WorkerInputs, ClickWorker
from window_init import MainWindow

ESC_KEY = 16777216


class AppWindow(MainWindow):

    worker_requested = pyqtSignal()
    change_inputs = pyqtSignal(WorkerInputs)

    def __init__(self, logger):
        super().__init__(logger)

        self.initialize_ui_connections()

        self.logger = logger
        self.esc_key_listener = None
        self.hotkey_listener = None
        self.location_click_listener = None
        self.mouse_controller = mouse.Controller()

        self.click_worker = ClickWorker
        self.worker_thread = QThread
        self.initialize_click_worker()

    def clear_simple_location(self):
        self.simple_location = None

    def clear_advanced_location(self):
        self.advanced_location = None

    def initialize_ui_connections(self):
        self.tab_wgt.currentChanged.connect(self.switched_tabs)
        self.smpl_hkey_keyseq.editingFinished.connect(self.hotkey_changed)
        self.smpl_hkey_keyseq.clear_callback = self.clear_simple_location
        self.smpl_hkey_keyseq.keySequenceChanged.connect(self.clear_hotkey)
        self.smpl_change_loc_btn.pressed.connect(self.change_location)
        self.adv_hkey_keyseq.editingFinished.connect(self.hotkey_changed)
        self.adv_hkey_keyseq.keySequenceChanged.connect(self.clear_hotkey)
        self.adv_hkey_keyseq.clear_callback = self.clear_advanced_location
        self.adv_change_loc_btn.pressed.connect(self.change_location)
        self.start_btn.clicked.connect(self.start_button_clicked)
        self.stop_btn.clicked.connect(self.stop_button_clicked)

    def initialize_click_worker(self):
        self.click_worker = ClickWorker(self.inputs, self.logger, self.mouse_controller)
        self.worker_thread = QThread()
        self.click_worker.finished.connect(self.stop_button_clicked)
        self.change_inputs.connect(self.click_worker.change_inputs)
        self.worker_requested.connect(self.click_worker.start)
        self.click_worker.moveToThread(self.worker_thread)

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

    def clear_hotkey_focus(self):
        if self.in_advanced_tab:
            self.adv_hkey_keyseq.clearFocus()
        else:
            self.smpl_hkey_keyseq.clearFocus()

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
            self.logger.error(f"Failed to set hotkey: {value}")
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

    def clear_hotkey(self):
        if self.current_hotkey:
            self.current_hotkey = None
        if self.hotkey_listener:
            self.hotkey_listener.stop()
            try:
                self.hotkey_listener.join()
            except RuntimeError:
                pass
            self.hotkey_listener = None

    @property
    def in_advanced_tab(self):
        return self.tab_wgt.currentIndex() == 1

    @property
    def inputs(self) -> WorkerInputs:
        inputs = WorkerInputs()
        if self.in_advanced_tab:
            if self.adv_clk_intvl_ledit.text() != "":
                inputs.interval = int(self.adv_clk_intvl_ledit.text())
            inputs.interval_scale_index = self.adv_clk_intvl_scale_cbox.currentIndex()
            if self.adv_clen_ledit.text() != "":
                inputs.hold_length = int(self.adv_clen_ledit.text())
            inputs.hold_length_scale_index = self.adv_clen_scale_cbox.currentIndex()
            if self.adv_clicks_per_event_ledit.text() != "":
                inputs.clicks_per_event = int(self.adv_clicks_per_event_ledit.text())
            inputs.event_count = (
                int(self.adv_clk_events_ledit.text())
                if self.adv_clk_events_ledit.text() != ""
                else None
            )
            inputs.location = self.advanced_location
            inputs.mouse_button_index = self.adv_mb_cbox.currentIndex()
        else:
            if self.smpl_clk_intvl_ledit.text() != "":
                inputs.interval = int(self.smpl_clk_intvl_ledit.text())
            inputs.interval_scale_index = self.smpl_clk_intvl_scale_cbox.currentIndex()
            inputs.location = self.simple_location
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

    def stop_click_worker(self):
        if self.worker_thread.isRunning():
            self.logger.info("Terminating worker thread")
            self.worker_thread.terminate()
            self.worker_thread.wait()

    @pyqtSlot()
    def start_button_clicked(self):
        if self.softlock_capable:
            self.logger.info("Displaying softlock prevention message")
            self.softlock_warning_msgb.exec()
            return
        self.stop_btn.setDisabled(False)
        self.start_btn.setDisabled(True)
        self.change_inputs.emit(self.inputs)
        self.worker_thread.start()
        self.worker_requested.emit()

    @pyqtSlot()
    def stop_button_clicked(self):
        self.stop_btn.setDisabled(True)
        self.start_btn.setDisabled(False)
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
            if self.worker_thread.isRunning()
            else self.start_button_clicked()
        )

    def clear_location_and_listener(self):
        self.logger.info("Clearing location value")
        self.stop_location_click_listener()
        self.stop_esc_key_listener()
        if self.in_advanced_tab:
            self.adv_loc_display_ledit.clear()
            self.advanced_location = None
            self.adv_change_loc_btn.setEnabled(True)
        else:
            self.smpl_loc_display_ledit.clear()
            self.simple_location = None
            self.smpl_change_loc_btn.setEnabled(True)

    def change_location(self):
        advanced_tab = self.in_advanced_tab

        def set_location():
            x, y = self.mouse_controller.position
            if advanced_tab:
                self.advanced_location = (x, y)
                self.adv_change_loc_btn.setEnabled(True)
                self.logger.info("Set advanced location to %s", self.advanced_location)
            else:
                self.simple_location = (x, y)
                self.smpl_change_loc_btn.setEnabled(True)
                self.logger.info("Set simple location to %s", self.simple_location)
            self.update_location_displays()
            self.stop_location_click_listener()
            self.stop_esc_key_listener()

        (
            self.adv_change_loc_btn.setEnabled(False)
            if advanced_tab
            else self.smpl_change_loc_btn.setEnabled(False)
        )

        (
            self.logger.info(
                "Listening for advanced location, waiting for click or esc press"
            )
            if advanced_tab
            else self.logger.info(
                "Listening for simple location, waiting for click or esc press"
            )
        )

        self.on_press_esc(self.clear_location_and_listener)
        sleep(0.2)
        self.on_location_click(set_location)

    def update_location_displays(self):
        if self.advanced_location is not None:
            self.adv_loc_display_ledit.setText(
                f"({self.advanced_location[0]}, {self.advanced_location[1]})"
            )
        if self.simple_location is not None:
            self.smpl_loc_display_ledit.setText(
                f"({self.simple_location[0]}, {self.simple_location[1]})"
            )
