import pyautogui
from mks import screenshot
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

def slowClick(x=-1, y=-1, sleep_seconds=0):
    if x != -1 and y != -1:
        mouseController.position = (x, y)
    mouseController.press(mouse.Button.left)
    pause(0.01)
    mouseController.release(mouse.Button.left)
    pause(sleep_seconds)

def mousePosition(x=None, y=None):
    if not x or not y:
        x, y = mouseController.position
        return floor(x), floor(y)
    mouseController.position = (x, y)

def press(char):
    pyautogui.press(char)

offsetMP = (0,0)
def offsetMousePos(x,y):
    global offsetMP
    offsetMP = (x,y)

def printMousePos():
    im = screenshot()
    xy = mousePosition()
    px = im.getpixel((xy[0]*2, xy[1]*2))
    xy = (xy[0]-offsetMP[0],xy[1]-offsetMP[1])
    print(f"xy: {xy} px: {px}")

running = True
def kknd():
    global running
    running = False

class Toggle():
    _active = False
    _timeout = .05
    _next_time = 0

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
        if self._timeout > 0 and self._next_time > time.time():
            return

        self._next_time = time.time() + self._timeout
        self._action()

class AutoClick(Toggle):
    _timeout = .05

    def _action(self):
        click()

clicker = AutoClick()

def loop(callback, hotkeys = {}):
    k = keyboard.GlobalHotKeys(
    {
        "c": clicker.toggle,
        "k": kknd,
        "p": printMousePos,
    } | hotkeys)
    k.start()

    while running:
        clicker.go()
        callback()
