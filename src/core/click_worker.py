import logging
import time
from typing import Callable

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QThread

from src.core.input import InputManager


class ClickWorkerManager(QObject):

    __worker_request = pyqtSignal(InputManager.WorkerInputs)

    def __init__(self, finished_callback: Callable):
        super().__init__()
        self.__click_worker: ClickWorker = ClickWorker()
        self.__worker_thread = QThread()

        self.__click_worker.finished.connect(finished_callback)
        self.__worker_request.connect(self.__click_worker.start)
        self.__click_worker.moveToThread(self.__worker_thread)

    def start(self, worker_inputs: InputManager.WorkerInputs):
        self.__worker_thread.start()
        self.__worker_request.emit(worker_inputs)

    def stop(self):
        if self.__worker_thread.isRunning():
            logging.info("Terminating worker thread")
            self.__worker_thread.terminate()
            self.__worker_thread.wait()

    @property
    def is_clicking(self) -> bool:
        return self.__worker_thread.isRunning()


class ClickWorker(QObject):

    finished = pyqtSignal()

    @pyqtSlot(InputManager.WorkerInputs)
    def start(self, worker_inputs: InputManager.WorkerInputs):
        try:
            logging.debug(f"Starting click worker with inputs {worker_inputs}")
            if worker_inputs.is_continuous:
                clicking = True
                while clicking:
                    self.__run_click_event(worker_inputs)
            else:
                for click_event in range(worker_inputs.event_count):
                    self.__run_click_event(worker_inputs)

            self.finished.emit()
        except Exception as e:
            logging.error(f"Error with click worker: {e}")
            self.finished.emit()

    @classmethod
    def __run_click_event(cls, worker_inputs: InputManager.WorkerInputs):

        if worker_inputs.is_using_location_x and worker_inputs.is_using_location_y:
            worker_inputs.mouse_controller.position = worker_inputs.location
        elif worker_inputs.is_using_location_x:
            worker_inputs.mouse_controller.position = (
                worker_inputs.location[0],
                worker_inputs.mouse_controller.position[1],
            )
        elif worker_inputs.is_using_location_y:
            worker_inputs.mouse_controller.position = (
                worker_inputs.mouse_controller.position[0],
                worker_inputs.location[1],
            )

        start_time = time.perf_counter()
        next_click_time = start_time + worker_inputs.interval
        for _ in range(worker_inputs.clicks_per_event):
            (
                cls.__held_click(worker_inputs)
                if worker_inputs.is_using_held_clicks
                else cls.__instant_click(worker_inputs)
            )
        remaining_time = max(0.0, next_click_time - time.perf_counter())
        if remaining_time > 0:
            time.sleep(remaining_time)

    @classmethod
    def __held_click(cls, worker_inputs: InputManager.WorkerInputs):
        worker_inputs.mouse_controller.press(worker_inputs.mouse_button)
        time.sleep(worker_inputs.hold_length)
        worker_inputs.mouse_controller.release(worker_inputs.mouse_button)

    @classmethod
    def __instant_click(cls, worker_inputs: InputManager.WorkerInputs):
        worker_inputs.mouse_controller.click(worker_inputs.mouse_button)
