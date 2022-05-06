from mk import click, press, printMousePos, loop, clicker, Toggle, mousePosition, pause
from mks import screenshot
import time
import math

gx = 392
gy = 208
state = {
    "game":{
        "x": gx,
        "y": gy,
        "w": 704,
        "h": 484,
    },
    "soldiers":{
        "x": 0,
        "y": 300,
        "w": 400,
        "h": 484-300,
    },
    "ammo_check": (35, 12),
    "ammo_color": (203, 209, 71),
    "upgrade_done_button": (488, 472),
    "buy_ammo": (71, 115),
    "buy_rifle": (367, 115),
    "buy_repair": (174, 115),
    "buy_wall": (282, 115),
    "buy_fortify": (479, 115),
    "buy_silo": (249, 316),
    #"soldier_color": (204,204,204),
    "soldier_color": (0,0,0),
    "shot_timeout": 1,
    "bubble": 30,
    "shots":[]
}


class Shots(Toggle):
    _timeout = .10

    def __init__(self):
        pass

    def _action(self):
        im = screenshot(state["game"]["x"], state["game"]["y"], state["game"]["w"], state["game"]["h"])

        upx = im.getpixel((state["upgrade_done_button"][0]*2, state["upgrade_done_button"][1]*2))
        if upx == (255,255,255) or upx == (62, 55, 41):
            print("upgrade")
            #return
            state["shots"] = []

            for i in range(10):
                click(state["game"]["x"] + state["buy_repair"][0],state["game"]["y"] + state["buy_repair"][1], .5)
            click(state["game"]["x"] + state["buy_rifle"][0],state["game"]["y"] + state["buy_rifle"][1], .5)
            #click(state["game"]["x"] + state["buy_silo"][0],state["game"]["y"] + state["buy_silo"][1], .5)

            for i in range(100):
                click(state["game"]["x"] + state["buy_ammo"][0],state["game"]["y"] + state["buy_ammo"][1], .2)

            click(state["game"]["x"] + state["buy_wall"][0],state["game"]["y"] + state["buy_wall"][1], .5)
            click(state["game"]["x"] + state["buy_fortify"][0],state["game"]["y"] + state["buy_fortify"][1], .5)

            click(state["game"]["x"] + state["upgrade_done_button"][0],state["game"]["y"] + state["upgrade_done_button"][1], .1)
            print("end upgrade")

        if im.getpixel((2*state["ammo_check"][0],state["ammo_check"][1]*2)) != state["ammo_color"]:
            press(" ")

        s = state["soldiers"]
        sx = 2 * s["x"]
        sy = 2 * s["y"]
        sw = 2 * s["w"]
        sh = 2 * s["h"]

        for y in range(sy, sy+sh, 4):
            for x in range(sx, sx+sw, 2):
                px = im.getpixel((x, y))
                if px == state["soldier_color"] and self.planShot(x, y):
                    shoot(x,y)
                    shoot(x,y)
                    state["shots"].append((x,y,time.time()+state["shot_timeout"]))

    def dist(self, x1, y1, x2, y2):
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)

    def planShot(self, x, y):
        for shot in state["shots"]:
            if self.dist(x, y, shot[0], shot[1]) < state["bubble"]:
                return False
        return True

shots = Shots()

def trimShots():
    ts = time.time()
    shots = [shot for shot in state["shots"] if ts < shot[2]]
    state["shots"] = shots

def shoot(x, y):
    click(
        x // 2 + state["game"]["x"] + 1,
        y // 2 + state["game"]["y"] + 10,
    )


hotkeys = {
    "t": shots.toggle,
}

def main():
    trimShots()
    shots.go()

print("Let's Storm the House")
loop(main, hotkeys=hotkeys)
