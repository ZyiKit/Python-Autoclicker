from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener, Button, Controller
from pynput import keyboard
import time
import threading
import random
import numpy as np


mouse_controller = Controller()

class Mac:

    def __init__(self, key, keybind, cps:float, toggle:bool, activated:bool): 
        self.key = key
        self.keybind = keybind
        self.cps = cps
        self.toggle = toggle
        self.activated = activated
        self.sleeping = self.calculate_overhead()

    def calculate_overhead(self):
        temp_cps = self.cps
        x = max(0, (1/temp_cps))
        x = round(x, 5)
        overhead = -(x**2) + (0.11*x) + 0.0015
        overhead = round(overhead, 5)
        sleeping = max(0, (1/temp_cps)) - overhead
        sleeping = round(sleeping, 5)
        print(f" x is {x}, {sleeping} is sleeping time, and {overhead} is overhead time") #debugging purposes
        return sleeping


#toggle = False means it is hold mode

FIRST = Mac(Button.left, Button.x2, 15, False, False)

SECOND = Mac(Button.right, Button.x1, 15, False, False)

macros = [FIRST, SECOND]


def random_calculate(sleeping):
    while True:
        sleepingrand = np.random.laplace(sleeping, sleeping*0.2)  #CPS INSTANTANEOUS SPEED DISTRIBUTION
        if sleepingrand <= 4*sleeping and sleepingrand >= sleeping*0.3:
            break
    return sleepingrand

def decay(sleeping):  #still need to activate it
    sleeping = random.uniform(sleeping*1.0005,sleeping*1.001)
    return sleeping
        
                
def perform_macro():

    while True:
        for m in macros:
            if True == m.activated:
                mouse_controller.click(m.key, 1)
                time.sleep(random_calculate(m.sleeping))
                
                
                


def on_press(keybind):

    for m in macros:
        try:
            if m.keybind == keybind:
                if m.toggle == True:
                    m.activated = not m.activated
                else:
                    m.activated = True
        except AttributeError:
            pass
        
    
def on_release(keybind):
    for m in macros:
        try:
            if m.keybind == keybind:
                if m.toggle == False:
                    m.activated = False
        except AttributeError:
            pass
        

def on_click(x,y,button, pressed):

    for m in macros:
        if m.keybind == button:
            if m.toggle == True:
                m.activated = not m.activated
            else:
                if pressed:
                    m.activated = True
                elif not pressed:
                    m.activated = False
        
    
            
                    
            



if __name__ == "__main__":

    threading.Thread(target=perform_macro, daemon=True).start()
    KB_listener = KeyboardListener(on_press=on_press, on_release=on_release)
    MO_listener = MouseListener(on_click=on_click)
    KB_listener.start()
    MO_listener.start()
    KB_listener.join()
    MO_listener.join()
    
