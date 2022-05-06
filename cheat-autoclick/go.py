from mk import clicker, loop


def makeFast():
    print("fast")
    clicker.type("fast")
def makeSlow():
    print("slow")
    clicker.type("slow")

hotkeys = {
    "f": makeFast,
    "s": makeSlow,
}

def main():
    return

print("Let's tap tap mine some bitcoin")
loop(main, hotkeys=hotkeys)
