from mk import click, press, printMousePos, loop, clicker, Toggle, mousePosition, pause
from mks import screenshot

game_pos = (284, 211)
game_dim = (922, 487)


class Floater(Toggle):
    _timeout = .05
    y_max=278
    y_min=205
    x = 333
    y = y_max
    y_step = 50

    def __init__(self, gamepos):
        self.y_max += gamepos[1]
        self.y_min += gamepos[1]
        self.x += gamepos[0]
        self.y = self.y_min

    def _action(self):
        self.y = min(self.y_max, self.y + self.y_step)
        self.y = max(self.y_min, self.y)
        if self.y_max == self.y or self.y == self.y_min:
            self.y_step =- self.y_step
        mousePosition(self.x, self.y)

floater = Floater(game_pos)


"""
auto_click = 50
cursor
auto_candy
steel_cursor
candy_farm
candy_mine
candy_factory
gold_cursor
candy_lab
candy_temple

candy_lab 40
candy_temple
diamond_cursor
candy_rocket
time_machine
candy_man
magic_cursor
candy_god
infinity
"""
class Buttons():
    """ buttons are located relative to the screenshot, not screen """
    we_are_on_top = True
    status = {"top": [], "bottom": [], "rebirth": ["off"]}
    rebirth = 0
    top = []
    bottom = []
    height = 50
    x = 682+222
    bottom_offset = 41

    def __init__(self):
        for i in range(10):
            self.top.append(i * self.height + 1)
            self.status["top"].append("off")
        for i in range(8):
            self.bottom.append(i * self.height + self.bottom_offset)
            self.status["bottom"].append("off")
        self.rebirth = 8 * self.height + self.bottom_offset + 2
        self.reset()

    def reset(self):
        for i in range(10):
            self.status["top"][i] = "off"
        for i in range(8):
            self.status["bottom"][i] = "off"
        self.status["rebirth"][0] = "off"


    def state(self, topbottom, index, state = "off"):
        self.status[topbottom][index] = state

    def areWeOnTop(self):
        self.we_are_on_top = self.status["top"][len(self.top)-1] == "off"
        return self.we_are_on_top

    def whereToClick(self):
        # find the last one pending
        # or find the last one "active"
        # click on it and 1 above
        how_many = 2
        last = how_many
        last_pending = -1
        last_active = -1

        if self.areWeOnTop():
            for i in range(len(self.top)):
                if self.status["top"][i] == "pending":
                    last_pending = i
                if self.status["top"][i] == "on":
                    last_active = i
            last = max(last_pending, last_active, how_many)

            if last < how_many:
                last = how_many
            r = []

            print(f"last_pending: {last_pending} | last_active: {last_active} | last: {last}")
            for i in range(how_many):
                r.append((self.x, self.top[last-i]))
            return r


        for i in range(len(self.bottom)):
            if self.status["bottom"][i] == "pending":
                last_pending = i
            if self.status["bottom"][i] == "on":
                last_active = i

        last = max(last_pending, last_active, how_many)
        print(f"last_pending: {last_pending} | last_active: {last_active} | last: {last}")
        r = []
        for i in range(how_many):
            r.append((self.x, self.bottom[last-i]))
        return r


buttons = Buttons()

class BuyUpgrades(Toggle):
    _timeout = 1
    scroll_up = (917, 3)
    scroll_dn = (917, 482)

    def __init__(self, gamepos, buttons):
        self.gamepos = gamepos
        self.buttons = buttons
        self.scroll_up = (self.scroll_up[0] + gamepos[0], self.scroll_up[1] + gamepos[1])
        self.scroll_dn = (self.scroll_dn[0] + gamepos[0], self.scroll_dn[1] + gamepos[1])

    def click(self, x, y, pause = .05, count = 1):
        for i in range(count):
            click(x, y, pause)

    def down(self):
        self.click(self.scroll_dn[0], self.scroll_dn[1], .05, 2)

    def up(self):
        self.click(self.scroll_up[0], self.scroll_up[1], .05, 2)

    def _action(self):
        if self.buttons.areWeOnTop():
            self.up()
        else:
            self.down()

        for i in self.buttons.whereToClick():
            self.click(i[0]+self.gamepos[0], i[1] + self.gamepos[1], count = 2)

upgrader = BuyUpgrades(gamepos = game_pos, buttons = buttons)

hack_is_panel_open = False
class Shots(Toggle):
    _timeout = 5
    color_active = (112, 188, 255)
    color_pending = (46, 77, 105)
    color_disabled = (15, 26, 35)

    def __init__(self, gamepos, gamedim, buttons):
        self.isopencheck = (451*2, 315*2)
        self.gamebox = (gamepos[0], gamepos[1], gamedim[0], gamedim[1])
        self.buttons = buttons

    def _action(self):
        im = screenshot(self.gamebox[0], self.gamebox[1], self.gamebox[2], self.gamebox[3])

        if self.buttons.areWeOnTop():
            for i in range(len(self.buttons.top)):
                #print(i)
                y = self.buttons.top[i] * 2
                px = im.getpixel((self.buttons.x*2, y))
                self.buttons.state("top", i, self.getPxState(px))
        else:
            for i in range(len(self.buttons.bottom)):
                y = self.buttons.bottom[i] * 2
                px = im.getpixel((self.buttons.x*2, y))
                self.buttons.state("bottom", i, self.getPxState(px))
            px = im.getpixel((self.buttons.x*2, self.buttons.rebirth*2))
            self.buttons.state("rebirth", 0, self.getPxState(px))
        print(f"analyzed buttons {self.buttons.status}")
        global hack_is_panel_open
        px = im.getpixel(self.isopencheck) 
        hack_is_panel_open = px == (255, 239, 69)
        print(f"is panel open {hack_is_panel_open} {px}")


    def getPxState(self, px):
        def inMargin(px, col):
            #print(px, col, px == col)
            return px == col
            for i in range(3):
                if px[i] == col[i]:
                    return True
                if col[i] + 3 > px[i] < col[i] -3:
                    return True

        if inMargin(px, self.color_disabled):
            return "off"
        if inMargin(px, self.color_active):
            return "on"
        return "pending"


shots = Shots(game_pos, game_dim, buttons)

class LevelUp(Toggle):
    _timeout = 10

    def __init__(self, gamepos):
        self.candy_per_click = (646+gamepos[0], 193+gamepos[1])
        self.candy_per_second = (646+gamepos[0], 248+gamepos[1])
        self.gold_candy = (646+gamepos[0], 304+gamepos[1])
        self.sugar = (646+gamepos[0], 356+gamepos[1])
        self.toggle = (534+gamepos[0], 107+gamepos[1])

    def _action(self):
        # toggle the level up field @todo
        global hack_is_panel_open
        print(f"Is panel open? {hack_is_panel_open}")
        if not hack_is_panel_open:
            click(self.toggle[0], self.toggle[1], .2)
            hack_is_panel_open = True

        print("buy level candy per click")
        click(self.candy_per_click[0], self.candy_per_click[1], .1)
        print("buy level sugar")
        click(self.sugar[0], self.sugar[1], .1)
        print("buy level gold candy")
        click(self.gold_candy[0], self.gold_candy[1], .1)
        print("buy level candy per second")
        click(self.candy_per_second[0], self.candy_per_second[1], .1)

leveler = LevelUp(game_pos)


class Rebirth(Toggle):
    _timeout = 5
    def __init__(self, gamepos, buttons):
        self.gamepos = gamepos
        self.confirmation = (510+gamepos[0], 305+gamepos[1])
        self.buttons = buttons

    def _action(self):
        if self.buttons.status["rebirth"][0] == "on":
            print("Rebirth")
            stopAll()
            click(self.buttons.x+self.gamepos[0], self.buttons.rebirth+self.gamepos[1], .4)
            click(self.confirmation[0], self.confirmation[1], .4)
            pause(1)
            self.buttons.reset()
            startAll()

rebirth = Rebirth(game_pos, buttons)

def startAll():
    floater.on()
    clicker.on()
    upgrader.on()
    shots.on()
    leveler.on()
    rebirth.on()

def stopAll():
    floater.off()
    clicker.off()
    upgrader.off()
    shots.off()
    leveler.off()
    rebirth.off()

hotkeys = {
    "p": printMousePos,
    "c": clicker.toggle,
    "f": floater.toggle,
    "u": upgrader._action,
    "s": shots._action,
    "l": leveler._action,
    "r": rebirth._action,
    "=": startAll,
    "-": stopAll,
}

def main():
    clicker.go()
    floater.go()
    upgrader.go()
    shots.go()
    leveler.go()
    rebirth.go()

print("Let's crush some candy too (2)")
loop(main, hotkeys=hotkeys)
