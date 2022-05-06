from mk import click, press, printMousePos, loop, clicker, Toggle, mousePosition, pause, slowClick, offsetMousePos
from mks import screenshot
import time
import math

gx = 183
gy = 203
#offsetMousePos(gx, gy)
state = {
    "url": "https://www.agame.com/game/bitcoin-tap-tap-mine",
    "game":{
        "x": gx,
        "y": gy,
        "w": 1061-gx,
        "h": 698-gy,
    },
    "box":(106+gx, 106+gy, 642+gx, 349+gy),
    "upgradesCheck": (143*2,435*2),
    "upgradesCheckColor": (148, 157, 152),
}

class MazeClicker(Toggle):
    _timeuout = 0
    y = 0
    x = 0
    step = 140
    nextCheck = 0
    checkDelay = 20

    def __init__(self):
        self.x = state["box"][0]
        self.y = state["box"][1]

    def _action(self):
        #self.checkUpgrades()
        self.x += self.step
        if self.x > state["box"][2]:
            self.x = state["box"][0]
            self.y += self.step
        if self.y > state["box"][3]:
            self.y = state["box"][1]

        slowClick(self.x, self.y)

    def checkUpgrades(self):
        if self.nextCheck > time.time():
            return
        pause(1)
        #open
        slowClick(247, 633,.5)
        pause(1)
        slowClick(944, 566, .5)
        pause(1)
        slowClick(537, 568, .5)
        pause(1)
        slowClick(953, 417, .5)
        pause(1)
        slowClick(529, 418, .5)
        pause(1)
        #close
        slowClick(988, 268,.5)
        pause(1)
        self.nextCheck = time.time() + self.checkDelay

mazeClicker = MazeClicker()

hotkeys = {
    "=": mazeClicker.toggle,
}

def main():
    mazeClicker.go()
    return

print("Let's tap tap mine some bitcoin")
loop(main, hotkeys=hotkeys)
