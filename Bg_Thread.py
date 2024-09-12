"""
 ____                        _   _
|  _ \ _____      _____ _ __| | | |_ __
| |_) / _ \ \ /\ / / _ \ '__| | | | '_ \
|  __/ (_) \ V  V /  __/ |  | |_| | |_) |
|_|   \___/ \_/\_/ \___|_|   \___/| .__/
                                  |_|

Perpetrated by © Osama Elazab since 2024
"""

import random
import time
import datetime
import threading

import pyautogui as pag

# Background thread that keeps the machine alive
class Live_Thread(threading.Thread):

    def __init__(self):
        # Call threading module constructor
        super().__init__()

        self.daemon = True

        # Drop the pyautogui failsafe checks
        pag.FAILSAFE = False

        # Execution periodicity for 'keep alive' activity
        self.refresh_time_s:int = 30
        self.threshold_time_ms:int = 900

        self.stop_thread:bool = False
        self.error:str = ''

    def generate_random_bool(self)-> bool:
        random_b:bool = random.choice([True,False])
        return random_b

    def get_current_timestamp(self)-> tuple[int,int]:
        current_time:datetime = datetime.datetime.now()
        current_seconds:int = current_time.second
        current_milliseconds: int = current_time.microsecond // 1000
        return current_seconds,current_milliseconds

    def press_ctrl(self)-> None:
        pag.press('ctrl')

    def press_shift(self)-> None:
        pag.hotkey('shift')

    # Executing background task based on a random order
    def execute_task(self)-> None:
        rand:bool = self.generate_random_bool()
        if rand:
            self.press_shift()
        else:
            self.press_ctrl()

    def terminate(self)-> None:
        self.stop_thread = True


    def run(self):
        # Thread infinite loop
        try:
            while True:

                # Terminate thread
                if self.stop_thread:
                    break

                # Execute the task each 'self.refresh_time' second, after 'threshold_time'
                seconds,milliseconds = self.get_current_timestamp()
                if (seconds % self.refresh_time_s == 0) and (milliseconds >= self.threshold_time_ms):
                    self.execute_task()

        except Exception as exp:
            self.error = str(exp)

