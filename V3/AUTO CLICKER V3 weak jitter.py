from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Button, Controller
import time
import threading
import random
mouse_controller = Controller()
print("Max cps is 200")
cps: float = input("Select a cps: ")
cps = float(cps)
overhead = 0.0012  # replace with whatever you measured
sleeping = max(0, (1/cps) - overhead)        # A new formula is used to calculate the sleeping time, f = 1/t idea is used
#with frequency = cps and t = time period per click, overhead is the processing time by CPU


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
            sleepingrand = random.uniform(max(0,(sleeping*0.6)), sleeping*1.40)
            time.sleep(sleepingrand)
        else:                           #Added this little part which drastically stabilises performance at high cps
            time.sleep(0.01)
            
      

threading.Thread(target=perform_macro, daemon=True).start()



with KeyboardListener(on_press=on_press) as listener:
    listener.join()

    



    
