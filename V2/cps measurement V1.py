import threading
from pynput import mouse
import time


count: int = int(0)


def main() -> None:
    
    user=input("Enter to start: ")
    global count
    count = 0
    start = time.perf_counter()
    lastshown = 0
    while True:
        elapsed = time.perf_counter()-start
        if elapsed >= 5.0:
            break
        shown = int(elapsed)
        if shown > lastshown:
            print(f"{shown} seconds has passed")
            lastshown = shown
        time.sleep(0.005)
        
            
        
        


        
    cps = count/5
    print(f"Total count is {count}")
    print(f"Your cps is {cps}")
            
def on_click(x, y, button, pressed):
    if pressed:
        global count
        count += 1

threading.Thread(target=main, daemon=True).start()

with mouse.Listener(on_click=on_click) as listener:
    listener.join()
