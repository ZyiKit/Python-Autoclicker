import threading
from pynput import mouse
import time
import sys

log_path: str = str(input("Enter file name to store values: "))
log_path: str = (log_path+'.txt')

clicklist = []
user = input("Enter to start: ")
print("Logging clicks... close the window or Ctrl+C to stop.")

def on_click(x, y, button, pressed):
    if pressed and (button == mouse.Button.left):
        clicklist.append(time.time())
    elif pressed and button == mouse.Button.right:
        with open(log_path, "a") as f:
                for ts in clicklist:
                    f.write(f"{ts}\n")
        print("documentation done!")
        listener.stop()
        
            
    
    
        






with mouse.Listener(on_click=on_click) as listener:
    listener.join()


