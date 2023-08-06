import ctypes
import subprocess
import sys
from datetime import datetime
from random import uniform
from time import perf_counter, sleep, time

import numpy as np
import pkg_resources
import psutil
import pyperclip
import win32gui
import win32process

from ninja_tools.bbox import BBOX

GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
GetWindowText = ctypes.windll.user32.GetWindowTextW


class Utilities:
    ##########################
    # Import functions
    ##########################
    @staticmethod
    def try_import(package, installer=None):
        def check(_):
            return _ in [_.project_name for _ in pkg_resources.working_set]

        if not check(package):
            installer = package if not installer else installer
            install = subprocess.Popen([sys.executable, "-m", "pip", "install", installer])
            install.wait()

    ##########################
    # Clipboard Functions
    ##########################
    @staticmethod
    def put_on_clipboard(_):
        pyperclip.copy(_)

    @staticmethod
    def get_from_clipboard():
        return pyperclip.paste()

    ##########################
    # Math Functions
    ##########################
    @staticmethod
    def safe_div(x, y):
        return 0 if y == 0 else x / y

    def safe_div_int(self, x, y):
        return int(self.safe_div(x, y))

    def safe_div_round(self, x, y, decimals=2):
        return round(self.safe_div(x, y), decimals)

    @staticmethod
    def get_distance(p0, p1):
        p0 = np.array(p0)
        p1 = np.array(p1)
        return np.linalg.norm(p0 - p1)

    def get_distance_int(self, p0, p1):
        return int(self.get_distance(p0, p1))

    def get_distance_rounded(self, p0, p1, decimals=0):
        return round(self.get_distance(p0, p1), decimals)

    ##########################
    # Process Functions
    ##########################
    @staticmethod
    def get_handle_from_title(window):
        return win32gui.FindWindow(None, window)

    @staticmethod
    def get_handle_from_pid(pid):
        def callback(hwnd, _):
            __, found_pid = win32process.GetWindowThreadProcessId(hwnd)

            if found_pid == pid:
                _.append(hwnd)
            return True

        handle = []
        win32gui.EnumWindows(callback, handle)
        return handle[0]

    @staticmethod
    def get_process_name_from_pid(pid):
        return psutil.Process(pid).name()

    def get_pid_from_title(self, window):
        handle = self.get_handle_from_title(window)
        _, found_pid = win32process.GetWindowThreadProcessId(handle)
        return found_pid

    @staticmethod
    def get_current_window_title():
        return win32gui.GetWindowText(win32gui.GetForegroundWindow())

    @staticmethod
    def get_current_window_pid():
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        return pid

    def get_window_title_from_pid(self, pid):
        handle = self.get_handle_from_pid(pid)
        return self.get_window_title_from_handle(handle)

    def is_current_window_title(self, window_name: str):
        return window_name == self.get_current_window_title()

    def is_current_window_pid(self, pid: int):
        return pid == self.get_current_window_pid()

    # Get current window pid

    @staticmethod
    def get_window_title_from_handle(hwnd):
        length = GetWindowTextLength(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowText(hwnd, buff, length + 1)
        return buff.value

    @staticmethod
    def _get_rect(type_, handle):
        if type_ == "WINDOW":
            return win32gui.GetWindowRect(handle)
        elif type_ == "CLIENT":
            return win32gui.GetClientRect(handle)
        else:
            raise 'Either type == WINDOW or CLIENT only!'

    def get_window_rect_from_handle(self, handle, bbox: bool = True):
        rect = self._get_rect("WINDOW", handle)
        return BBOX(rect) if bbox else rect

    def get_window_rect_from_pid(self, pid, bbox: bool = True):
        handle = self.get_handle_from_pid(pid)
        rect = self._get_rect("WINDOW", handle)
        return BBOX(rect) if bbox else rect

    def get_client_rect_from_handle(self, handle, bbox: bool = True):
        rect = self._get_rect("CLIENT", handle)
        return BBOX(rect) if bbox else rect

    def get_client_rect_from_pid(self, pid, bbox: bool = True):
        handle = self.get_handle_from_pid(pid)
        rect = self._get_rect("CLIENT", handle)
        return BBOX(rect) if bbox else rect

    # Get all pid of process with same names
    @staticmethod
    def get_pids_from_process_name(process_name):
        return [_.pid for _ in psutil.process_iter() if _.name() == process_name]

    # # Get all pid of process with same names using window name
    @staticmethod
    def get_pids_from_window_title(window_title):
        def callback(hwnd, hwnd_list_):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) == window_title:
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                hwnd_list_.append(found_pid)
            return True

        hwnd_list = []
        win32gui.EnumWindows(callback, hwnd_list)
        return hwnd_list

    ##########################
    # Utility Functions
    ##########################
    @staticmethod
    def find(input_, string, options=any, contains=True):
        """
        A function that checks if a given string contains or does not contain one or more items from a list or a
        single item.
        :param input_: A list of items or a single item
        :param string: The string to be checked
        :param options: A function that defines how to check the items in the list (default: any)
        :param contains: A flag to indicate whether to check if the items are in the string or not (default: True)
        :return: Boolean value indicating whether the string contains or does not contain the items

        Example:
        # Check if the string "Hello World" contains any of the items in the list ["Hello", "Goodbye"]
        result = find(["Hello", "Goodbye"], "Hello World")
        print(result) # True

        # Check if the string "Hello World" contains all of the items in the list ["Hello", "Goodbye"]
        result = find(["Hello", "Goodbye"], "Hello World", all)
        print(result) # False
        """
        # Check if input_ is a list
        if isinstance(input_, list):
            # Check if we are checking if the string contains the items or not
            if contains:
                # Use the options function to check if any or all of the items are in the string
                return options(item in string for item in input_)
            else:
                # Use the options function to check if any or all of the items are not in the string
                return options(item not in string for item in input_)
        else:
            # If input_ is not a list, check if it's in the string or not
            if contains:
                return string in input_
            else:
                return input_ not in string

    @staticmethod
    def pause(milliseconds: int):
        sleep(milliseconds * 0.001)

    @staticmethod
    def humanly_press():
        sleep_time = uniform(0.25, 0.3)  # random float between 250-300 ms
        sleep(sleep_time)

    @staticmethod
    def make_hash(d):
        __ = ''
        for _ in d:
            __ += str(d[_])
        return hash(__)

    @staticmethod
    def timestamp():
        (dt, micro) = datetime.utcnow().strftime('%Y%m%d-%H%M%S.%f').split('.')
        dt = "%s.%03d" % (dt, int(micro) * 0.001)
        return dt

    @staticmethod
    def timestamp2():
        # Output format: 2020-01-01 00:00:00
        return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def datetime():
        return datetime.utcnow()

    @staticmethod
    def perf():
        return perf_counter()

    @staticmethod
    def time():
        return time()

    ##########################
    # I/O
    ##########################
    @staticmethod
    def write_to_file(filename, text, method: str = "a", add_new_line: bool = True):
        with open(filename, method) as file:
            if add_new_line:
                file.write(text + "\n")
            else:
                file.write(text)

    @staticmethod
    def read_file(filename, method="r"):
        return open(filename, method).read()

    @staticmethod
    def read_lines(filename, method="r"):
        return open(filename, method, encoding="utf8").readlines()

    ##########################
    # Assorted
    ##########################
    @staticmethod
    def cv2_show(cv2, image, window_name=None, delay=1, stop_key='q'):
        cv2.imshow(window_name, image)
        if cv2.waitKey(delay) & 0xFF == ord(stop_key):
            cv2.destroyAllWindows()

    # def timeout(self, key, ms):
    #     if key in self.timeouts:
    #         return self.timeouts[key].timeout(ms)
    #
    #     else:
    #         self.timeouts[key] = ProcessTime()
    #         return False
