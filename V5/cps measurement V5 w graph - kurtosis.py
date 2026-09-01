import threading
from pynput import mouse
import time
import sys
import matplotlib.pyplot as plt

from scipy.stats import kurtosis



def first_click(x, y, button, pressed):
    if pressed and (button == mouse.Button.left):
        print("Starting to record clicks....")
        listener.stop()
    

def plot_graph():
    global goodlist 
    x1=[]
    y1=[]
    x2=[]
    y2=[]
    for index, value in enumerate(goodlist):
        if index > 0:
            x1.append(value-goodlist[0])
            y1.append(index/(value-goodlist[0]))
            x2.append(value-goodlist[0])
            y2.append(1/(value-goodlist[index-1]))
    print(y2)
    plt.xlabel("Instantaneous cps")
    plt.ylabel("Probability density")
    plt.title("Instantaneous distribution")
    plt.hist(y2, bins='fd', density=True, alpha=0.5)
    plt.show()
    excess_kurt = kurtosis(y2, fisher=True)
    print(f"Excess kurtosis: {excess_kurt}")
 
    
                          


def one_click(x, y, button, pressed):
    if pressed and (button == mouse.Button.left):
        clicklist.append(time.time())
    elif pressed and button == mouse.Button.right:
        if len(clicklist) > 2:
            global goodlist
            goodlist = clicklist
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
        else:
            print("Not enough clicks recorded - need more clicks")




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

        

        plot_graph()
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
            i=input("Enter to terminate")
            break
       
                
            
                    

