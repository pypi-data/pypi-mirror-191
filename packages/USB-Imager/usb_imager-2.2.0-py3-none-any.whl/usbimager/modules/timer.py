# -*- coding: utf-8 -*-
"""Timer class."""

import time


class Timer:
    """Timer in seconds."""

    def __init__(self):

        self.start_time = 0.0
        self.stop_time = 0.0
        self.start_time_cpu = 0.0
        self.stop_time_cpu = 0.0

    @property
    def result(self) -> str:
        return self.stop_time - self.start_time

    @property
    def result_cpu(self) -> str:
        return self.stop_time_cpu - self.start_time_cpu

    def start(self) -> None:
        self.start_time = time.time()
        self.start_time_cpu = time.process_time()

    def stop(self) -> None:
        self.stop_time = time.time()
        self.stop_time_cpu = time.process_time()

    def reset(self) -> None:
        self.start_time = 0.0
        self.stop_time = 0.0
        self.start_time_cpu = 0.0
        self.stop_time_cpu = 0.0
