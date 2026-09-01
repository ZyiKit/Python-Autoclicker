from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Button, Controller
import time
import threading

mouse_controller = Controller()
print("Max cps is 90.0")
cps: float = input("Select a cps: ")
cps = float(cps)
sleeping = (1-(cps*0.011))/cps



toggle = False
def on_press(key):
    global toggle
    try:
        if key.char == 'p':
            toggle = not toggle
            print(f"Macro is now: {'ON' if toggle else 'OFF'}")
    except AttributeError:
        pass


def perform_macro():
    global sleeping
    while True:
        if toggle:
            mouse_controller.click(Button.left, 1)
            time.sleep(sleeping)
            
        time.sleep(0.01)

threading.Thread(target=perform_macro, daemon=True).start()



with KeyboardListener(on_press=on_press) as listener:
    listener.join()

    



    
