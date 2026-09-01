import threading
from pynput import mouse
import time
import sys




def first_click(x, y, button, pressed):
    if pressed and (button == mouse.Button.left):
        print("Starting to record clicks....")
        listener.stop()
    



def one_click(x, y, button, pressed):
    if pressed and (button == mouse.Button.left):
        clicklist.append(time.time())
    elif pressed and button == mouse.Button.right:
        firsttime = clicklist[0]
        lasttime = clicklist[-1]
        timetaken: float = float(lasttime-firsttime)
        print(f"Time taken is {timetaken}")
        print(f"Total clicks: {len(clicklist)}")
        print(clicklist)
        global cps
        cps = float(len(clicklist))/timetaken
        print(f"Cps measured is {cps}")
                                     
                                
                        
        listener.stop()




if __name__ == "__main__":

    fileq: str = str(input("Do you want a file to record cps?(Yes/No)"))
    fileq:str = fileq.lower()
    while True:
        if (fileq == 'yes') or (fileq == 'no'):
            if fileq == 'yes':
                
                namefile:str = str(input("Name the file"))
                with open(namefile, "a") as f:
                    f.write(f"CPS Measured\n")
            break
        else:
            fileq:str = str(input("Please enter 'Yes' or 'No' only"))
            fileq:str = fileq.lower()
    
            


    while True:   
        clicklist = []
        user = input("Enter to start: ")
        print("Left click to start recording... Right Click to stop.")
                
        with mouse.Listener(on_click=first_click) as listener:
            listener.join()
        with mouse.Listener(on_click=one_click) as listener:
            listener.join()
            end: str = (str(input("Do you want to take another cps measurement?(Yes/No)")))
            end: str = end.lower()
            while True:
                if (end == 'yes') or (end == 'no'):
                    if fileq == 'yes':
                        with open (namefile, "a") as f:
                            f.write(f"{cps}\n")
                    break                                
                else:
                    end:str = str(input("Please enter 'Yes' or 'No' only"))
                    end: str = end.lower()
                
            if end == 'no':
                break
       
                
            
                    

