from mss import mss
from PIL import Image

def screenshot(x, y, width, height):
    mon = {
        "top": y,
        "left": x,
        "width": width,
        "height": height
    }
    with mss() as sct:
        sct_img = sct.grab(mon)
    return Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")


def getPixelAt(x, y, img):
    return img.getpixel((x, y))
