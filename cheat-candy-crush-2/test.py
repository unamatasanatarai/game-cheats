import pyautogui
import time
from pynput import keyboard, mouse
from PIL import ImageGrab

mc = mouse.Controller()
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

def get_mouse_coordinates():
    print(pyautogui.position())


candy_y_max=555
candy_y_min=359
candy_x = 385

scroll_up = (1023, 214)
scroll_dn = (1023, 707)
button_h = 55
buttons_x = 837
buttons_y = [
    205+(0*button_h),
    205+(1*button_h),
    205+(2*button_h),
    205+(3*button_h),
    205+(4*button_h),
    205+(5*button_h),
    205+(6*button_h),
    205+(7*button_h),
    205+(8*button_h),
    205+(9*button_h),
]
k = keyboard.GlobalHotKeys({
    "p": get_mouse_coordinates
})
k.start()

def main():

    while running:
        #im = ImageGrab.grab(bbox=(0,0,640,480))
        #print(im.getpixel((100,100)))
        pass

main()
exit()

image = ImageGrab.grab(bbox=(10, 10, 300, 300))
print(image.format, image.size, image.mode)
image.save("/tmp/abc.png")
exit()
for y in range (0, 100, 10):
    for x in range (0, 100, 10):
        color = image.getpixel((x, y))
        print(color);
