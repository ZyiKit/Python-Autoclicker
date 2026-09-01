
import json

cps = 15
keybind = 'MouseButton.x2'
Killswitch = 'f7'
Mode = 1
ClickButton = 'MouseButton.right'


def save_file(filename="settings.json"):
    global cps, keybind, Killswitch, Mode, ClickButton
    settings = {"cps": cps, "keybind": keybind, "Killswitch": Killswitch, "Mode":Mode, "ClickButton":ClickButton}
    with open (filename, 'w') as json_file:
        json.dump(settings, json_file)

def load_file(filename="settings.json"):
    global cps, keybind, Killswitch, Mode, ClickButton
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        cps = data["cps"]
        keybind = data["keybind"]
        Killswitch = data["Killswitch"]
        Mode = data["Mode"]
        ClickButton = data["ClickButton"]
    
    
save_file()
load_file()
