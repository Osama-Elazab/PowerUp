"""
 ____                        _   _
|  _ \ _____      _____ _ __| | | |_ __
| |_) / _ \ \ /\ / / _ \ '__| | | | '_ \
|  __/ (_) \ V  V /  __/ |  | |_| | |_) |
|_|   \___/ \_/\_/ \___|_|   \___/| .__/
                                  |_|

Perpetrated by © Osama Elazab since 2024
"""

import time
import datetime
import keyboard
import threading
import logging
import sys
import os

import colorama as cma
from Bg_Thread import Live_Thread

# The CLI handler class
class CLI_handler:
    # To enable debug
    debug_mode = False

    def __init__(self):

        # Event to control the printing
        self.printing_event: bool = False
        self.timer_counter: int = 0
        self.clear_command: str = 'clear' if os.name == 'posix' else 'cls'

        # State of timer
        self.timer_state: str = 'stopped'

        self.bg_thread = None
        self.fg_process = None

        self.stop_fg: bool = False

        self.sep_char: str = '*'
        self.sep_line: str = ''

        # Keyboard shortcuts
        self.start_sc: str = 'alt+q'
        self.pause_sc: str = 'alt+w'
        self.stop_sc: str = 'alt+e'
        self.exit_sc: str = 'esc'
        self.abort_sc: str = 'ctrl+c'
        self.menu_options: str = ''

        # Start logging (activated in debugging mode only)
        self.logger = self.setup_logger(name='main',log_file='app.log')
        self.logger.info("------------- [ Start of logging ] -------------")

        # Initialize colorama package
        cma.init()

        # Initialize CLI internal functionality
        self.init_cli()



    # Setup logger (for debugging purpose only)
    def setup_logger(self, name:str, log_file:str) -> logging.Logger:

        # Only enable logger when debug mode is activated
        log_level = logging.INFO if CLI_handler.debug_mode else logging.CRITICAL+1

        # File handler
        if CLI_handler.debug_mode:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
            file_handler = logging.FileHandler(log_file, 'w')
            file_handler.setFormatter(formatter)

        # Basic logger
        logger = logging.getLogger(name)
        logger.setLevel(log_level)
        if CLI_handler.debug_mode: logger.addHandler(file_handler)

        return logger

    def init_fg_thread(self) -> None:
        # Start the fg thread when printing_event is set
        self.fg_process = threading.Thread(target=self.main_loop)
        self.fg_process.daemon = True
        self.fg_process.start()
        self.logger.info("Foreground thread is signaled")

    def init_cli(self) -> None:
        try:
            self.init_fg_thread()
            self.construct_sep_line()
            self.construct_menu_options()

            # Default timer screen
            self.reset_timer_screen()
            self.logger.info("CLI is initialized successfully")

        except Exception as exp:
            self.logger.critical("Error in CLI initialization phase:")
            self.logger.critical(f"{str(exp)}")

    def construct_sep_line(self) -> None:
        self.sep_line: str = f"{self.sep_char}{30 * self.sep_char}{self.sep_char}"

    def construct_menu_options(self) -> None:
        self.menu_options: str = f"{cma.Fore.GREEN}{self.sep_char}  {self.start_sc.upper()}  -> start timer       {self.sep_char}\n" + \
                                 f"{cma.Fore.YELLOW}{self.sep_char}  {self.pause_sc.upper()}  -> pause timer       {self.sep_char}\n" + \
                                 f"{cma.Fore.RED}{self.sep_char}  {self.stop_sc.upper()}  -> stop timer        {self.sep_char}\n" + \
                                 f"{cma.Fore.CYAN}{self.sep_char}  {self.exit_sc.upper()}    -> exit program      {self.sep_char}\n" + \
                                 f"{cma.Fore.MAGENTA}{self.sep_char}  {self.abort_sc.upper()} -> abort program     {self.sep_char}\n" + \
                                 f"{cma.Fore.BLUE}{self.sep_line}{cma.Style.RESET_ALL}"

    def clear_screen(self) -> None:
        os.system(self.clear_command)

    def get_elapsed_time(self, timer) -> str:
        days, remainder = divmod(timer, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        result = f"{days:02}:{hours:02}:{minutes:02}:{seconds:02}"
        return result


    def show_goodbye_message(self)-> None:
        self.clear_screen()

        bye_string :str= """

        *****    *    *  *****
        *     *   *  *   *
        *****      **    *****
        *     *     *    *
        ******      *    *****

        """

        goodbye_message:str = f"{cma.Fore.LIGHTCYAN_EX}" +\
                              f"{bye_string}" +\
                              f"{cma.Style.RESET_ALL}"

        print(goodbye_message)

    # get the timer box color based on current execution state
    def get_timer_bg(self) -> str:
        if self.timer_state == 'running':
            bg = cma.Fore.LIGHTGREEN_EX
        elif self.timer_state == 'paused':
            bg = cma.Fore.YELLOW
        elif self.timer_state == 'stopped':
            bg = cma.Fore.RED
        else:
            raise ValueError("Out of bound timer state !!!")

        return bg

    def construct_timer_txt(self, cnt: int) -> str:
        current_time: str = self.get_elapsed_time(cnt)

        timer_bg: str = self.get_timer_bg()

        timer_mini_window: str = f"{timer_bg}" + \
                                 f"{self.sep_line}\n" + \
                                 f"{self.sep_char}         {current_time}          {self.sep_char}\n" + \
                                 f"{self.sep_line}{cma.Style.RESET_ALL}\n"

        return timer_mini_window

    def print_timer_window(self, counter: int) -> None:
        timer_txt: str = self.construct_timer_txt(counter)
        # Construct static + dynamic timer window into one window
        window_txt: str = timer_txt + self.menu_options
        self.clear_screen()
        
        print(window_txt)

    # Print the timer screen
    def main_loop(self) -> None:
        # Thread infinite loop
        while True:
            try:
                # Stop ongoing thread
                if self.stop_fg:
                    break

                t1:float = time.perf_counter()

                if self.printing_event:
                    self.timer_counter += 1
                    self.print_timer_window(self.timer_counter)
                    self.logger.info("Background thread is now running...")

                t2:float = time.perf_counter()

                remaining:float = 1 - (t2 - t1)
                time.sleep(remaining)

            # For abnormal process termination
            except KeyboardInterrupt:
                break

            except Exception as exp:
                self.logger.error("Error in foreground thread:")
                self.logger.error(f"{str(exp)}")

    def terminate_fg_thread(self) -> None:
        self.stop_fg = True

    def reset_timer_screen(self) -> None:
        self.print_timer_window(0)

    def start_printing(self) -> None:
        self.printing_event = True

    def stop_printing(self) -> None:
        self.printing_event = False

    def reset_timer_counter(self) -> None:
        self.timer_counter = 0

    def start_bg_task(self) -> None:
        if not self.bg_thread:
            self.bg_thread = Live_Thread()
            self.bg_thread.start()

    def stop_fg_thread(self) -> None:
        if self.fg_process:
            self.terminate_fg_thread()
            self.fg_process = None

    def stop_bg_thread(self) -> None:
        if self.bg_thread:
            self.bg_thread.terminate()
            self.bg_thread = None

    def stop_all_threads(self) -> None:
        self.stop_fg_thread()
        self.stop_bg_thread()

    # Start background thread
    def start(self) -> None:
        if not self.bg_thread:
            self.timer_state = 'running'
            self.start_bg_task()
            self.start_printing()
            self.logger.info("Background thread started")

    # Pause background thread
    def pause(self) -> None:
        if self.bg_thread:
            self.timer_state = 'paused'
            self.stop_bg_thread()
            self.stop_printing()
            self.clear_screen()
            self.print_timer_window(self.timer_counter)
            self.logger.info("Background thread paused")

    # Kill background thread
    def stop(self) -> None:
        self.timer_state = 'stopped'
        self.stop_bg_thread()
        self.stop_printing()
        self.reset_timer_counter()
        self.clear_screen()
        self.reset_timer_screen()
        self.logger.info("All threads stopped")


    def exit_list(self) -> None:
        self.stop_all_threads()
        self.logger.info("Application is closing")
        self.logger.info("------------- [ End of logging ] -------------")
        self.show_goodbye_message()
        sys.exit(0)

    def show_cli(self) -> None:
        try:
            # Bind the key shortcuts events
            keyboard.add_hotkey(self.start_sc, self.start)
            keyboard.add_hotkey(self.pause_sc, self.pause)
            keyboard.add_hotkey(self.stop_sc, self.stop)

            # Keep the program running to listen for 'esc' key presses
            keyboard.wait('esc')

            # Make sure to execute exit list before closing
            self.exit_list()

        # To abort program
        except KeyboardInterrupt:
            self.exit_list()

        except Exception as exp:
            self.logger.error("Error in foreground thread:")
            self.logger.error(f"{str(exp)}")


def main()-> None:
    CLI_handler().show_cli()

# Entry point
if __name__ == "__main__":
    main()


