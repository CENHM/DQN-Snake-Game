import ctypes
import random
import threading
import time

import win32api
import win32con



import ctypes
from ctypes import wintypes, windll

INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEY_EVENT_KEYUP = 0x0002

ESC = 27
ENTER = 13

LEFT = 65
UP = 87
RIGHT = 68
DOWN = 83

LEFT_UP = 87
RIGHT_UP = 69
LEFT_DOWN = 83
RIGHT_DOWN = 68


def ReleaseKey(user, hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEY_EVENT_KEYUP))
    user.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def PressKey(user, hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def press_esc():
    win32api.keybd_event(ESC, 0, 0, 0)
    win32api.keybd_event(ESC, 0, win32con.KEYEVENTF_KEYUP, 0)


def press_nothing():
    time.sleep(0.01)


def press_left():
    win32api.keybd_event(LEFT, 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(LEFT, 0, win32con.KEYEVENTF_KEYUP, 0)


def press_up():
    win32api.keybd_event(UP, 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(UP, 0, win32con.KEYEVENTF_KEYUP, 0)


def press_right():
    win32api.keybd_event(RIGHT, 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(RIGHT, 0, win32con.KEYEVENTF_KEYUP, 0)


def press_down():
    win32api.keybd_event(DOWN, 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(DOWN, 0, win32con.KEYEVENTF_KEYUP, 0)


def press_left_up():
    win32api.keybd_event(LEFT_UP, 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(LEFT_UP, 0, win32con.KEYEVENTF_KEYUP, 0)


def press_right_up():
    win32api.keybd_event(RIGHT_UP, 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(RIGHT_UP, 0, win32con.KEYEVENTF_KEYUP, 0)


def press_left_down():
    win32api.keybd_event(LEFT_DOWN, 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(LEFT_DOWN, 0, win32con.KEYEVENTF_KEYUP, 0)


def press_right_down():
    win32api.keybd_event(RIGHT_DOWN, 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(RIGHT_DOWN, 0, win32con.KEYEVENTF_KEYUP, 0)


actions = [press_right, press_left, press_up, press_down,
           press_left_up, press_right_up, press_left_down, press_right_down]


# Run the action
def take_action(action):
    actions[action]()


# INPUT_MOUSE = 0
# INPUT_KEYBOARD = 1
# INPUT_HARDWARE = 2

# KEYEVENTF_EXTENDEDKEY = 0x0001
# KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
# KEYEVENTF_SCANCODE = 0x0008
MAPVK_VK_TO_VSC = 0

wintypes.ULONG_PTR = wintypes.WPARAM


class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx", wintypes.LONG),
                ("dy", wintypes.LONG),
                ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))


class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk", wintypes.WORD),
                ("wScan", wintypes.WORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            user32 = ctypes.WinDLL('user32', use_last_error=True)
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg", wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))


class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))

    _anonymous_ = ("_input",)
    _fields_ = (("type", wintypes.DWORD),
                ("_input", _INPUT))