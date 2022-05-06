import pyautogui
import time
from math import floor
from pynput import keyboard, mouse

mouseController = mouse.Controller()

def pause(seconds):
    time.sleep(seconds)

def click(x=-1, y=-1, sleep_seconds=0):
    if x != -1 and y != -1:
        mouseController.position = (x, y)
    mouseController.click(mouse.Button.left)
    pause(sleep_seconds)

def mousePosition(x=None, y=None):
    if not x or not y:
        x, y = mouseController.position
        return floor(x), floor(y)
    mouseController.position = (x, y)

def press(char):
    pyautogui.press(char)

def printMousePos():
    print(mousePosition())

running = True
def kknd():
    global running
    running = False

class Toggle():
    _active = False
    _timeout = .05
    _last_time = 0

    def on(self):
        self._active = True
        return self

    def off(self):
        self._active = False
        return self

    def toggle(self):
        self._active = not self._active
        return self

    def _action(self):
        pass

    def go(self):
        if not self._active:
            return
        if self._last_time + self._timeout > time.time():
            return

        self._last_time = time.time()
        self._action()

class AutoClick(Toggle):
    _timeout = .05

    def _action(self):
        click()

clicker = AutoClick()

def loop(callback, hotkeys = {}):
    k = keyboard.GlobalHotKeys(
    {
        "k": kknd
    } | hotkeys)
    k.start()

    while running:
        callback()
