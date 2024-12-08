from time import sleep

import mouse
import keyboard
from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal, QThread

from click_process import ClickProcessInputs, ClickProcess, AdvancedClickProcess
from window_init import MainWindow


class FinishedSignalEmitter(QObject):
    finished_signal = pyqtSignal()


class AppWindow(MainWindow):
    def __init__(self):
        super().__init__()
        self._finished_emitter = FinishedSignalEmitter()
        self._finished_emitter.finished_signal.connect(self.stop_button_clicked)
        self._current_click_process = None

    def clear_hotkey(self):
        key_sequence_edit = self.sender()
        if 16777216 in list(key_sequence_edit.keySequence()):
            key_sequence_edit.clearFocus()
            self.smpl_hkey_keyseq.clear()
            self.adv_hkey_keyseq.clear()
            if self.current_hotkey:
                keyboard.unhook_all_hotkeys()
            self.current_hotkey = None

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
            self.softlock_warning_msgb.exec()
            return
        self.active_process = True
        self.stop_btn.setDisabled(False)
        self.start_btn.setDisabled(True)
        ClickProcess.terminate_all()
        click_process = ClickProcess.get_appropriate(self.inputs)
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
        ClickProcess.terminate_all()

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
        ClickProcess.terminate_all()

    @pyqtSlot()
    def hotkey_changed(self):
        sender = self.sender()
        if sender == self.smpl_hkey_keyseq:
            self.adv_hkey_keyseq.setKeySequence(self.smpl_hkey_keyseq.keySequence())
        elif sender == self.adv_hkey_keyseq:
            self.smpl_hkey_keyseq.setKeySequence(self.adv_hkey_keyseq.keySequence())
        key_sequence = sender.keySequence().toString()
        if key_sequence:
            key_sequence = str(key_sequence).replace(" ", "").lower()
            if self.current_hotkey:
                keyboard.unhook_all_hotkeys()
            self.current_hotkey = keyboard.add_hotkey(key_sequence, self.hotkey_toggle)

    def closeEvent(self, event):
        keyboard.unhook_all()
        mouse.unhook_all()
        event.accept()

    def hotkey_toggle(self):
        (
            self.stop_button_clicked()
            if self.active_process
            else self.start_button_clicked()
        )

    def change_location(self):
        advanced_tab = self.in_advanced_tab

        def set_location():
            x, y = mouse.get_position()
            if advanced_tab:
                self.advanced_location = (x, y)
                self.adv_change_loc_btn.setEnabled(True)
            else:
                self.simple_location = (x, y)
                self.smpl_change_loc_btn.setEnabled(True)
            self.update_location_displays()
            mouse.unhook_all()

        (
            self.adv_change_loc_btn.setEnabled(False)
            if advanced_tab
            else self.smpl_change_loc_btn.setEnabled(False)
        )
        sleep(0.2)
        mouse.on_click(set_location)

    def update_location_displays(self):
        if self.advanced_location is not None:
            self.adv_loc_display_ledit.setText(
                f"({self.advanced_location[0]}, {self.advanced_location[1]})"
            )
        if self.simple_location is not None:
            self.smpl_loc_display_ledit.setText(
                f"({self.simple_location[0]}, {self.simple_location[1]})"
            )
