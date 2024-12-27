import logging
import time
from dataclasses import dataclass
from typing import Optional, Tuple

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from pynput.mouse import Button


@dataclass
class WorkerInputs:
    interval: int = 100
    interval_scale_index: int = 0
    hold_length: int = 0
    hold_length_scale_index: int = 0
    clicks_per_event: int = 1
    event_count: Optional[int] = None
    location: Optional[Tuple[int, int]] = None
    mouse_button_index: int = 0

    @staticmethod
    def timescale_from_index(index: int) -> float:
        match index:
            case 0:  # Milliseconds
                return 0.001
            case 1:  # Seconds
                return 1.0
            case 2:  # Minutes
                return 60.0
            case 3:  # Hours
                return 3600.0

    @property
    def interval_scale(self) -> float:
        return self.timescale_from_index(self.interval_scale_index)

    @property
    def length_scale(self) -> float:
        return self.timescale_from_index(self.hold_length_scale_index)

    @property
    def scaled_interval(self) -> float:
        return self.interval * self.interval_scale

    @property
    def scaled_hold_length(self) -> float:
        return self.hold_length * self.length_scale

    @property
    def is_using_location(self) -> bool:
        return self.location is not None

    @property
    def is_held_click(self) -> bool:
        return self.hold_length > 0

    @property
    def is_infinite(self) -> bool:
        return self.event_count is None

    @property
    def location_x(self) -> int:
        return self.location[0] if self.is_using_location else None

    @property
    def location_y(self) -> int:
        return self.location[1] if self.is_using_location else None

    @property
    def mouse_button(self) -> Button:
        match self.mouse_button_index:
            case 0:
                return Button.left
            case 1:
                return Button.right
            case 2:
                return Button.middle

    def __str__(self):
        return (
            f"interval={self.scaled_interval}, "
            f"length={self.scaled_hold_length}, "
            f"event_count={self.event_count}, "
            f"clicks_per_event={self.clicks_per_event}, "
            f"mouse_button={self.mouse_button}, "
            f"location={self.location}"
        )


class ClickWorker(QObject):

    finished = pyqtSignal()

    def __init__(self, inputs: WorkerInputs, mouse_controller):
        super().__init__()
        self.inputs = inputs
        self.mouse_controller = mouse_controller

    @pyqtSlot(WorkerInputs)
    def change_inputs(self, inputs: WorkerInputs):
        self.inputs = inputs

    @pyqtSlot()
    def start(self):
        try:

            def click_event():
                if self.inputs.is_using_location:
                    self.move_to_location(
                        self.inputs.location_x, self.inputs.location_y
                    )

                self.interval_wrapper(self.inputs.scaled_interval)

            logging.info(f"Starting click worker: {str(self.inputs)}")
            if self.inputs.is_infinite:
                while True:
                    click_event()
            else:
                for _ in range(self.inputs.event_count):
                    click_event()

            self.finished.emit()
        except Exception as e:
            logging.error(f"Error with click worker: {e}")
            self.finished.emit()

    def move_to_location(self, x: int, y: int) -> None:
        self.mouse_controller.position = (x, y)

    def interval_wrapper(self, interval: float):
        start_time = time.perf_counter()
        next_click_time = start_time + interval
        for _ in range(self.inputs.clicks_per_event):
            (
                self.held_click(
                    self.inputs.mouse_button, self.inputs.scaled_hold_length
                )
                if self.inputs.is_held_click
                else self.instant_click(self.inputs.mouse_button)
            )
        remaining_time = max(0.0, next_click_time - time.perf_counter())
        if remaining_time > 0:
            time.sleep(remaining_time)

    def held_click(self, mouse_button: Button, hold_length: float):
        self.mouse_controller.press(mouse_button)
        time.sleep(hold_length)
        self.mouse_controller.release(mouse_button)

    def instant_click(self, mouse_button: Button):
        self.mouse_controller.click(mouse_button)
