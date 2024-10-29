import datetime
import multiprocessing
import time

import mouse

import pyautogui


class ClickProcess(multiprocessing.Process):
    def __init__(
            self,
            click_interval: str,
            interval_timescale: str,
            click_length: str,
            length_timescale: str,
            mouse_button: str,
            clicks_per_event: str,
            click_events: str,
            click_location_string: str,
            terminated_event: multiprocessing.Event
    ):
        if click_interval == "":
            click_interval = 0
        else:
            click_interval = int(click_interval)

        if click_length == "":
            click_length = 0
        else:
            click_length = int(click_length)

        if clicks_per_event == "":
            clicks_per_event = 1
        else:
            clicks_per_event = int(clicks_per_event)

        if click_events == "":
            click_events = 0
        else:
            click_events = int(click_events)

        match interval_timescale:
            case "1":
                self.click_interval = float(datetime.timedelta(milliseconds=click_interval).total_seconds())
            case "2":
                self.click_interval = float(click_interval)
            case "3":
                self.click_interval = float(datetime.timedelta(minutes=click_interval).total_seconds())
            case "4":
                self.click_interval = float(datetime.timedelta(hours=click_interval).total_seconds())

        match length_timescale:
            case "1":
                self.click_length = float(datetime.timedelta(milliseconds=click_length).total_seconds())
            case "2":
                self.click_length = float(click_length)
            case "3":
                self.click_length = float(datetime.timedelta(minutes=click_length).total_seconds())
            case "4":
                self.click_length = float(datetime.timedelta(hours=click_length).total_seconds())

        match mouse_button:
            case "1":
                self.mouse_button = mouse.LEFT
            case "2":
                self.mouse_button = mouse.RIGHT
            case "3":
                self.mouse_button = mouse.MIDDLE

        self.interval_timescale = interval_timescale
        self.length_timescale = length_timescale
        self.clicks_per_event = clicks_per_event
        self.click_events = click_events
        self.terminated_event = terminated_event

        self.using_location = click_location_string != "none"

        if self.using_location:
            click_location = click_location_string.strip('()').split(',')
            self.click_location_x = int(float(click_location[0]))
            self.click_location_y = int(float(click_location[1]))

        pyautogui.MINIMUM_DURATION = 0.0
        pyautogui.PAUSE = 0.0

        super().__init__(target=self.click_process, daemon=True)

    def click_event(self) -> None:
        start_time = time.perf_counter()
        next_click_time = start_time + self.click_interval
        if self.using_location:
            pyautogui.moveTo(self.click_location_x, self.click_location_y, _pause=False)
        for _ in range(self.clicks_per_event):
            mouse.click(self.mouse_button)
        remaining_time = max(0.0, next_click_time - time.perf_counter())
        if remaining_time > 0:
            time.sleep(remaining_time)

    def held_click_event(self):
        start_time = time.perf_counter()
        next_click_time = start_time + self.click_interval
        if self.using_location:
            pyautogui.moveTo(self.click_location_x, self.click_location_y, _pause=False)
        mouse.press(self.mouse_button)
        time.sleep(self.click_length)
        mouse.release(self.mouse_button)
        remaining_time = max(0.0, next_click_time - time.perf_counter())
        if remaining_time > 0:
            time.sleep(remaining_time)

    def click_process(self) -> None:
        try:
            if self.click_length > 0:
                click_event = self.held_click_event
            else:
                click_event = self.click_event

            if self.click_events == 0:
                while True:
                    click_event()
            else:
                for _ in range(self.click_events):
                    click_event()
                self.terminated_event.set()
        except Exception as error:
            print(f"Click process error: {error}")
            self.terminated_event.set()
            return
