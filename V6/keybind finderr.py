#KEYBIND FINDER FOR OBSCURE KEYS
from pynput.mouse import Listener as MouseListener, Button

def on_click(x, y, button, pressed):
    if button == Button.x1:
        print("buttonfirst")
    elif button == Button.x2:
        print("buttonsecond")

#def on_click(x, y, button, pressed):
#   print(button)

with MouseListener(on_click=on_click) as listener:
    listener.join()


# Button.x1 Button.x2
