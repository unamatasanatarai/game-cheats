from mss import mss
from PIL import Image

def screenshot(x=None, y=None, width=None, height=None):
    mon = {
        "top": y,
        "left": x,
        "width": width,
        "height": height
    }
    with mss() as sct:
        if x is None:
            sct_img = sct.grab(sct.monitors[1])
        else:
            sct_img = sct.grab(mon)
    return Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")


def getPixelAt(x, y, img):
    return img.getpixel((x, y))
