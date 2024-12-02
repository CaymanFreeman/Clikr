import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from multiprocessing import Process
from typing import Optional, Tuple, Callable

import mouse
import pyautogui


@dataclass
class ClickProcessInputs:
    is_advanced: bool = False
    click_interval: int = 100
    click_interval_scale_index: int = 0
    click_length: int = 0
    click_length_scale_index: int = 0
    clicks_per_event: int = 1
    click_events: Optional[int] = None
    click_location: Optional[Tuple[int, int]] = None
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
    def click_interval_scale(self) -> float:
        return self.timescale_from_index(self.click_interval_scale_index)

    @property
    def click_length_scale(self) -> float:
        return self.timescale_from_index(self.click_length_scale_index)

    @property
    def scaled_click_interval(self) -> float:
        return self.click_interval * self.click_interval_scale

    @property
    def scaled_click_length(self) -> float:
        return self.click_length * self.click_length_scale

    @property
    def has_location(self) -> bool:
        return self.click_location is not None

    @property
    def location_x(self) -> int:
        return self.click_location[0] if self.has_location else None

    @property
    def location_y(self) -> int:
        return self.click_location[1] if self.has_location else None

    @property
    def mouse_button_str(self):
        match self.mouse_button_index:
            case 0:
                return mouse.LEFT
            case 1:
                return mouse.RIGHT
            case 2:
                return mouse.MIDDLE


class ClickProcess(ABC):

    @staticmethod
    def get_appropriate(inputs: ClickProcessInputs):
        return (
            AdvancedClickProcess(inputs)
            if inputs.is_advanced
            else SimpleClickProcess(inputs)
        )

    @abstractmethod
    @property
    def appropriate_process_type(self) -> Callable[[], None]:
        pass

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def click_process(self) -> None:
        pass

    @abstractmethod
    def location_click_process(self) -> None:
        pass


class SimpleClickProcess(ClickProcess):

    __slots__ = [
        "click_interval",
        "mouse_button",
        "location_x",
        "location_y",
    ]

    def __init__(self, inputs: ClickProcessInputs):
        self.click_interval = inputs.scaled_click_interval
        self.mouse_button = inputs.mouse_button_str
        self.location_x = inputs.location_x
        self.location_y = inputs.location_y

    @property
    def appropriate_process_type(self) -> Callable[[], None]:
        return (
            self.location_click_process
            if self.location_x is not None
            else self.click_process
        )

    def start(self) -> None:
        Process(target=self.appropriate_process_type, daemon=True)

    def click_process(self) -> None:
        while True:
            self.run_click_event()

    def location_click_process(self) -> None:
        while True:
            pyautogui.moveTo(self.location_x, self.location_x, _pause=False)
            self.run_click_event()

    def run_click_event(self) -> None:
        start_time = time.perf_counter()
        next_click_time = start_time + self.click_interval
        mouse.click(self.mouse_button)
        remaining_time = max(0.0, next_click_time - time.perf_counter())
        if remaining_time > 0:
            time.sleep(remaining_time)


class AdvancedClickProcess(ClickProcess):

    __slots__ = [
        "click_interval",
        "click_length",
        "clicks_per_event",
        "click_events",
        "mouse_button",
        "location_x",
        "location_y",
    ]

    def __init__(self, inputs: ClickProcessInputs):
        self.click_interval = inputs.scaled_click_interval
        self.click_length = inputs.scaled_click_length
        self.clicks_per_event = inputs.clicks_per_event
        self.click_events = inputs.click_events
        self.mouse_button = inputs.mouse_button_str
        self.location_x = inputs.location_x
        self.location_y = inputs.location_y

    @property
    def appropriate_process_type(self) -> Callable[[], None]:
        return (
            self.location_click_process
            if self.location_x is not None
            else self.click_process
        )

    def start(self) -> None:
        Process(target=self.appropriate_process_type, daemon=True)

    def click_process(self) -> None:
        if self.click_length > 0:
            click_event = self.run_held_click_event
        else:
            click_event = self.run_click_event

        if self.click_events is None:
            while True:
                click_event()
        else:
            for _ in range(self.click_events):
                click_event()

    def location_click_process(self) -> None:
        if self.click_length > 0:
            click_event = self.run_held_click_event
        else:
            click_event = self.run_click_event

        def move():
            pyautogui.moveTo(self.location_x, self.location_x, _pause=False)

        if self.click_events is None:
            while True:
                move()
                click_event()
        else:
            for _ in range(self.click_events):
                move()
                click_event()

    def run_click_event(self) -> None:
        start_time = time.perf_counter()
        next_click_time = start_time + self.click_interval
        for _ in range(self.clicks_per_event):
            mouse.click(self.mouse_button)
        remaining_time = max(0.0, next_click_time - time.perf_counter())
        if remaining_time > 0:
            time.sleep(remaining_time)

    def run_held_click_event(self) -> None:
        start_time = time.perf_counter()
        next_click_time = start_time + self.click_interval
        mouse.press(self.mouse_button)
        time.sleep(self.click_length)
        mouse.release(self.mouse_button)
        remaining_time = max(0.0, next_click_time - time.perf_counter())
        if remaining_time > 0:
            time.sleep(remaining_time)
