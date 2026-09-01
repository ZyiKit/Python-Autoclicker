from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Button, Controller
import time
import threading
import random
import numpy as np



mouse_controller = Controller()
print("Max cps is 200")
cps: float = input("Select a cps: ")
cps = float(cps)
overhead = 0.0012  # replace with whatever you measured
sleeping = max(0, (1/cps) - overhead)        # A new formula is used to calculate the sleeping time, f = 1/t idea is used
#with frequency = cps and t = time period per click, overhead is the processing time by CPU

toggleorhold = 'hold' # 'toggle' is for toggle activation while 'hold' is for hold activation type of macro
keybind = 'p'

activated = False
def on_press_toggle(key):
    global activated
    try:
        if key.char == keybind:
            activated = not activated
            print(f"Macro is now: {'ON' if activated else 'OFF'}")
    except AttributeError:
        pass

def on_press_hold(key):
    global activated
    try:
        if key.char == keybind:
            activated = True
    except AttributeError:
        pass



def on_release_hold(key):
    global activated
    try:
        if key.char == keybind:
            activated = False
    except AttributeError:
        pass

def perform_macro():
    global sleeping
    while True:
        if activated:
            mouse_controller.click(Button.left, 1)
            while True:
                sleepingrand = np.random.laplace(sleeping, sleeping*0.2)  #CPS INSTANTANEOUS SPEED DISTRIBUTION
                if sleepingrand <= 4*sleeping and sleepingrand >= sleeping*0.3:
                    break
            time.sleep(sleepingrand)
            sleeping = random.uniform(sleeping*1.0005,sleeping*1.001) #CPS DECAY
        else:                           #Added this little part which drastically stabilises performance at high cps
            time.sleep(0.01)
            

threading.Thread(target=perform_macro, daemon=True).start()   

if toggleorhold == 'toggle':
    with KeyboardListener(on_press=on_press_toggle) as listener:
        listener.join()
elif toggleorhold == 'hold':
    with KeyboardListener(on_press=on_press_hold, on_release=on_release_hold) as listener:
        listener.join()

    

    



    
