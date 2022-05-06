import pyautogui
import time
from pynput import keyboard, mouse

mc = mouse.Controller()

def get_mouse_coordinates():
    print(pyautogui.position())

__x = 0;
__y = 0;
def store_mouse_pos():
    global __x, __y
    __x, __y = pyautogui.position()

def restore_mouse_pos():
    click(__x, __y)

def click(x=-1,y=-1):
    if x == -1 or y == -1:
        pyautogui.click()
    else:
        pyautogui.click(x,y)

def press(char):
    pyautogui.press(char)

running=True
def kknd():
    global running
    running=False




## V2 - toggles
skip_top_houses = False
flood_buy_all = False
flood_buy_houses = False
flood_ascend = False
flood_mouse_float = False
flood_mouse_click = False
flood_q = False
flood_w = False

flood_buy_all_prev = False
flood_buy_houses_prev = False
flood_ascend_prev = False
flood_mouse_float_prev = False
flood_mouse_click_prev = False


# W
def toggle_w():
    global flood_w
    flood_w = not flood_w
    print(f"flood_w :: {flood_w}")

# Q
def toggle_q():
    global flood_q
    flood_q = not flood_q
    print(f"flood_q :: {flood_q}")

# buy all
def toggle_flood_buy_all():
    global flood_buy_all
    flood_buy_all = not flood_buy_all
    print(f"flood_buy_all :: {flood_buy_all}")

# buy houses
def toggle_flood_buy_houses():
    global flood_buy_houses
    flood_buy_houses = not flood_buy_houses
    print(f"flood_buy_houses :: {flood_buy_houses}")

# ascend
def toggle_flood_ascend():
    global flood_ascend
    flood_ascend = not flood_ascend
    print(f"flood_ascend :: {flood_ascend}")

# mouse floating
def toggle_mouse_float():
    global flood_mouse_float
    flood_mouse_float = not flood_mouse_float
    print(f"flood_mouse_float :: {flood_mouse_float}")

def off_mouse_float():
    global flood_mouse_float, flood_mouse_float_prev
    flood_mouse_float_prev = flood_mouse_float
    flood_mouse_float = False
    print(f"flood_mouse_float :: {flood_mouse_float}")

def on_mouse_float():
    global flood_mouse_float
    flood_mouse_float = flood_mouse_float_prev
    print(f"flood_mouse_float :: {flood_mouse_float}")


# mouse clicking
def toggle_mouse_click():
    global flood_mouse_click
    flood_mouse_click = not flood_mouse_click
    print(f"flood_mouse_click :: {flood_mouse_click}")

def off_mouse_click():
    global flood_mouse_click, flood_mouse_click_prev
    flood_mouse_click_prev = flood_mouse_click
    flood_mouse_click = False
    print(f"flood_mouse_click :: {flood_mouse_click}")

def on_mouse_click():
    global flood_mouse_click
    flood_mouse_click = flood_mouse_click_prev
    print(f"flood_mouse_click :: {flood_mouse_click}")

## V2 - actions
float_drag=0
float_drag_step=40
float_drag_max=80
def do_mouse_float():
    if not flood_mouse_float:
        return

    global float_drag, float_drag_step
    if float_drag < -float_drag_max or float_drag > float_drag_max:
        float_drag_step = -float_drag_step
    float_drag += float_drag_step
    mc.position = (454, 548+float_drag)

def do_mouse_click():
    if not flood_mouse_click:
        return
    click()

## V2 buy all
magic_steps = ["all", "all", "houses"]
magic_step = 0
t_magic = 3
t_magic_next = time.time() + t_magic
def do_buy_all():
    global t_magic_next
    print("Buy all")
    off_mouse_float()
    off_mouse_click()
    store_mouse_pos()

    press("2")
    click(1478, 278)

    restore_mouse_pos()
    on_mouse_float()
    on_mouse_click()
    t_magic_next = time.time() + t_magic

def can_buy_all():
    if not flood_buy_all or magic_steps[magic_step] != "all":
        return False
    return time.time() > t_magic_next


## V2 buy houses
def do_buy_houses():
    global t_magic_next
    print("Buy houses")
    press("e")
    off_mouse_float()
    off_mouse_click()
    store_mouse_pos()

    press("1")
    click(1235, 940)
    click(1235, 833)
    if not skip_top_houses:
        click(1235, 735)
        click(1235, 625)
        click(1235, 514)
        click(1235, 411)
        click(1235, 307)
    #click to scroll to bottom
    click(1589, 975)

    time.sleep(0.3)
    restore_mouse_pos()
    on_mouse_float()
    on_mouse_click()

    press("e")
    t_magic_next = time.time() + t_magic

def can_buy_houses():
    if not flood_buy_houses or magic_steps[magic_step] != "houses":
        return False
    return time.time() > t_magic_next



## V2 - ascend
t_ascend = 60*10
t_ascend_next = time.time() + t_ascend
t_skip_top_houses = 2 * 60
skip_top_houses_t = time.time() + t_skip_top_houses
def do_ascend():
    print("Ascend")
    global t_ascend_next, skip_top_houses_t
    stop_all()

    press("3")
    click(1418, 322)
    click(1376, 804)

    t_ascend_next = time.time() + t_ascend
    skip_top_houses_t = time.time() + t_skip_top_houses

    start_all()

def can_ascend():
    if not flood_ascend:
        return False
    return time.time() > t_ascend_next

## V2 Q
t_q = 10
t_q_next = time.time() + t_q

def can_q():
    if not flood_q:
        return False
    return time.time() > t_q_next

def do_q():
    print("q")
    global t_q_next
    press("q")
    t_q_next = time.time() + t_q

## V2 W
t_w = 10
t_w_next = time.time() + t_w

def can_w():
    if not flood_w:
        return False
    return time.time() > t_w_next

def do_w():
    print("w")
    global t_w_next
    press("w")
    t_w_next = time.time() + t_w


def start_all():
    global flood_buy_all, flood_buy_houses, flood_ascend, flood_mouse_float, flood_mouse_click, flood_q, flood_w
    flood_buy_all= flood_buy_houses= flood_ascend= flood_mouse_float= flood_mouse_click= flood_q= flood_w = True

def stop_all():
    global flood_buy_all, flood_buy_houses, flood_ascend, flood_mouse_float, flood_mouse_click, flood_q, flood_w
    flood_buy_all= flood_buy_houses= flood_ascend= flood_mouse_float= flood_mouse_click= flood_q= flood_w = False


k = keyboard.GlobalHotKeys({
    'k': kknd,
    'b': toggle_flood_buy_all,
    'h': toggle_flood_buy_houses,
    'a': toggle_flood_ascend,
    'f': toggle_mouse_float,
    'c': toggle_mouse_click,
    'r': toggle_q,
    's': toggle_w,
    '=': start_all,
    '-': stop_all,
    '^': do_ascend,

    'p': get_mouse_coordinates,
    #'b': buy_all,
    #'h': buy_houses,
    #'a': ascend,
    })
k.start()


def main():
    print("Let's cheat tap ninja")
    global magic_step, skip_top_houses

    while running:
        skip_top_houses = time.time() > skip_top_houses_t

        step_magic = False
        do_mouse_float()
        do_mouse_click()

        if can_q():
            do_q()

        if can_w():
            do_w()

        if can_buy_all():
            do_buy_all()
            step_magic = True

        if can_buy_houses():
            do_buy_houses()
            step_magic = True

        if step_magic:
            magic_step += 1
            if magic_step >= len(magic_steps):
                magic_step = 0

        if can_ascend():
            do_ascend()

main()
