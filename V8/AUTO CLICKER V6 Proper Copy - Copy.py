from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener, Button, Controller
from pynput import keyboard
import time
import threading
import random
import numpy as np



mouse_controller = Controller()

cps: float = input("Select a cps: ")
cps = float(cps)

toggleorhold = 'hold' # 'toggle' is for toggle activation while 'hold' is for hold activation type of macro
keybind = Button.x2
activated = False



x = max(0, (1/cps))
x = round(x, 5)
overhead = -(x**2) + (0.11*x) + 0.0015
overhead = round(overhead, 5)
sleeping = max(0, (1/cps)) - overhead
# A new formula is used to calculate the sleeping time, f = 1/t idea is used
#with frequency = cps and t = time period per click, overhead is the processing time by CPU

sleeping = round(sleeping, 5)
setsleeping = sleeping


#print(f" x is {x}, {sleeping} is sleeping time, and {overhead} is overhead time") #for debugging purposes


global activated, sleeping, keybind


def on_press_toggle(key):

    if key == keyboard.Key.f7: #Users should be able to pick kill switch
        KB_listener.stop()
        MO_listener.stop()
        return
    try:
        if key.char == keybind:
            if not activated:
                sleeping = setsleeping
            activated = not activated
            print(f"Macro is now: {'ON' if activated else 'OFF'}")

    except AttributeError:
        pass

def on_press_hold(key):

    if key == keyboard.Key.f7:         #Users should be able to pick kill switch
        KB_listener.stop()
        MO_listener.stop()
        return
    try:
        if key.char == keybind:
            activated = True
            sleeping = setsleeping
    except AttributeError:
        pass



def on_release_hold(key):

    try:
        if key.char == keybind:
            activated = False
    except AttributeError:
        pass
    
def on_press_mousecon(x,y,button, pressed):

    if button == keybind:
        if toggleorhold == 'toggle':
            activated = not activated
            if not activated:
                sleeping = setsleeping
        elif toggleorhold == 'hold':
            if pressed:
                activated = True
                sleeping = setsleeping
            elif not pressed:
                activated = False


def perform_macro():

    while True:
        if activated:
            mouse_controller.click(Button.left, 1)  #Button.left should be a variable that users can pick
            while True:
               sleepingrand = np.random.laplace(sleeping, sleeping*0.2)  #CPS INSTANTANEOUS SPEED DISTRIBUTION
               if sleepingrand <= 4*sleeping and sleepingrand >= sleeping*0.3:
                   break
            time.sleep(sleeping)
            sleeping = random.uniform(sleeping*1.0005,sleeping*1.001) #CPS DECAY
        else:                           #Added this little part which drastically stabilises performance at high cps
            time.sleep(0.01)
            





if __name__ == "__main__":

    threading.Thread(target=perform_macro, daemon=True).start()   

    if toggleorhold == 'toggle':
        KB_listener = KeyboardListener(on_press=on_press_toggle)
        MO_listener = MouseListener(on_click=on_press_mousecon)

        KB_listener.start()
        MO_listener.start()
        KB_listener.join()
        MO_listener.join()
            
    elif toggleorhold == 'hold':
        KB_listener = KeyboardListener(on_press=on_press_toggle, on_release=on_release_hold)
        MO_listener = MouseListener(on_click=on_press_mousecon)


        KB_listener.start()
        MO_listener.start()
        KB_listener.join()
        MO_listener.join()
        

    



    
