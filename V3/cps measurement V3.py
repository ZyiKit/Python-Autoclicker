import threading
from pynput import mouse
import time
import sys


clicklist = []
user = input("Enter to start: ")
print("Logging clicks... Right Click to stop.")






def on_click(x, y, button, pressed):
    if pressed and (button == mouse.Button.left):
        clicklist.append(time.time())
    elif pressed and button == mouse.Button.right:
        firsttime = clicklist[0]
        lasttime = clicklist[-1]
        timetaken: float = float(lasttime-firsttime)
        print(f"Time taken is {timetaken}")
        print(f"Total clicks: {len(clicklist)}")
        print(clicklist)
        cps: float = float(len(clicklist))/timetaken
        print(f"Cps measured is {cps}")
                                     
                                
                        
        listener.stop()
        
            
    
    
        




with mouse.Listener(on_click=on_click) as listener:
    listener.join()


