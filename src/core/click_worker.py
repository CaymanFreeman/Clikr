"""Provides the click worker to process click operations for Clikr"""

import logging
import time
from functools import lru_cache
from typing import NamedTuple, Optional, Callable, override

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
from pynput.mouse import Button as MouseButton, Controller as MouseController


class MousePosition(NamedTuple):
    """Coordinate pair for a mouse's position on the screen."""

    x: int
    y: int


class WorkerInputs(NamedTuple):
    """Collection of inputs for a click worker."""

    interval: float
    hold_length: float
    clicks_per_event: int
    event_count: int | None
    mouse_button: MouseButton
    location: tuple[Optional[int], Optional[int]]
    is_using_location_x: bool
    is_using_location_y: bool
    is_using_held_clicks: bool
    is_continuous: bool
    mouse_controller: MouseController

    @override
    def __str__(self) -> str:
        """Returns the string representation of the current relevant inputs."""
        return (
            f"(interval={self.interval}, "
            f"hold_length={self.hold_length}, "
            f"clicks_per_event={self.clicks_per_event}, "
            f"event_count={self.event_count}, "
            f"mouse_button={self.mouse_button.name}, "
            f"location={self.location})"
        )


class ClickWorkerManager(QObject):
    """Manages the click worker thread and coordinates click operations."""

    worker_request: pyqtSignal = pyqtSignal(WorkerInputs)

    def __init__(self, finished_callback: Callable[[], None]) -> None:
        super().__init__()
        self.__click_worker: ClickWorker = ClickWorker()
        self.__worker_thread = QThread()

        self.__click_worker.finished.connect(finished_callback)
        self.worker_request.connect(self.__click_worker.start)
        self.__click_worker.moveToThread(self.__worker_thread)

    def start(self, worker_inputs: WorkerInputs) -> None:
        """Initializes and starts the click worker thread."""
        self.__worker_thread.start()
        self.worker_request.emit(worker_inputs)

    def stop(self) -> None:
        """Terminates the click worker thread if it is running."""
        if self.__worker_thread.isRunning():
            logging.debug("Terminating worker thread")
            self.__worker_thread.terminate()
            self.__worker_thread.wait()


class ClickWorker(QObject):
    """Executes click operations based on worker inputs."""

    finished = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.__last_position: Optional[MousePosition] = None

    @pyqtSlot(WorkerInputs)
    def start(self, worker_inputs: WorkerInputs) -> None:
        """Starts the click worker with the provided worker inputs."""
        try:
            logging.debug("Starting click worker with inputs %s", worker_inputs)

            if worker_inputs.is_continuous:
                clicking: bool = True
                while clicking:
                    self._execute_click_event(worker_inputs)
            else:
                assert isinstance(worker_inputs.event_count, int)
                for _ in range(worker_inputs.event_count):
                    self._execute_click_event(worker_inputs)

            self.finished.emit()

        except InterruptedError as error:
            logging.error("Click worker was interrupted: %s", error)
            self.finished.emit()

    def _execute_click_event(self, worker_inputs: WorkerInputs) -> None:
        """Executes a click event based on the provided worker inputs."""
        start_time = time.perf_counter()

        self._move_to_target(worker_inputs)

        for _ in range(worker_inputs.clicks_per_event):
            self._execute_click(worker_inputs)

        next_click_time = start_time + worker_inputs.interval
        remaining_time = next_click_time - time.perf_counter()
        if remaining_time > 0:
            time.sleep(remaining_time)

    @classmethod
    def _execute_click(cls, worker_inputs: WorkerInputs) -> None:
        """Executes a click or held click based on the provided worker inputs."""
        if worker_inputs.is_using_held_clicks:
            worker_inputs.mouse_controller.press(worker_inputs.mouse_button)
            time.sleep(worker_inputs.hold_length)
            worker_inputs.mouse_controller.release(worker_inputs.mouse_button)
        else:
            worker_inputs.mouse_controller.click(worker_inputs.mouse_button)

    @lru_cache(maxsize=30)
    def _calculate_next_position(
        self,
        current_x: int,
        current_y: int,
        target_x: Optional[int],
        target_y: Optional[int],
    ) -> MousePosition:
        """Calculates the next mouse position for a click event."""
        new_x = target_x if target_x is not None else current_x
        new_y = target_y if target_y is not None else current_y
        return MousePosition(new_x, new_y)

    def _move_to_target(self, worker_inputs: WorkerInputs) -> None:
        """Moves the mouse to the target location if it is not already there."""
        if not (worker_inputs.is_using_location_x or worker_inputs.is_using_location_y):
            return

        controller_position = worker_inputs.mouse_controller.position
        current_position = MousePosition(*controller_position)

        if current_position == self.__last_position:
            return

        next_position = self._calculate_next_position(
            current_position.x,
            current_position.y,
            worker_inputs.location[0],
            worker_inputs.location[1],
        )

        worker_inputs.mouse_controller.position = (next_position.x, next_position.y)
        self.__last_position = next_position
