from tkinter import *
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener, Button as MouseButton, Controller
from pynput import keyboard
import time
import threading
import random
import numpy as np
import json
import os
import sys


#Use Button as MouseButton to not cause conflict with tkinter Button, tkinter has too much code to edit

window = Tk()

window.geometry("350x450")
window.title("Python Autoclicker")

# Ensure the software doesn't crash when image doesn't load
try:
    icon = PhotoImage(file='python_logo.png')
    window.iconphoto(True, icon)
except Exception:
    pass

#CPS STUFF
cps = 10.0
sleeping = 0.1
setsleeping = 0.1

#OTHER VARIABLES
keybind = None
Killswitch = None
Mode = 0 # 0 is hold, 1 is toggle
ClickButton = 0 # 0 is left, 1 is right , 2 is middle mouse button
activated = None
keybind_select = 'None'



#FOR CPS INPUT
def submit():
    global sleeping, cps, setsleeping
    try:
        cps = float(entry.get())
    except ValueError:
        CPS_label.config(text='Invalid CPS value: {}'.format(cps))
        return 
    CPS_label.config(text='Current CPS: {}'.format(cps))
    cps = float(cps)
    sleeping, setsleeping = calculate_sleeping(cps)


def calculate_sleeping(cps):
    x = max(0, (1/cps))
    x = round(x, 5)
    overhead = -(x**2) + (0.11*x) + 0.0015
    overhead = round(overhead, 5)
    sleeping = max(0, (1/cps)) - overhead
    # A new formula is used to calculate the sleeping time, f = 1/t idea is used
    #with frequency = cps and t = time period per click, overhead is the processing time by CPU
    sleeping = round(sleeping, 5)
    setsleeping = sleeping
    save_file()

    return sleeping, setsleeping


#print(f" x is {x}, {sleeping} is sleeping time, and {overhead} is overhead time") #for debugging purposes

#Function to save file
def save_file(filename="settings.json"):
    global cps, keybind, Killswitch, Mode, ClickButton
    settings = {"cps": float(cps), "keybind": str(keybind), "Killswitch": str(Killswitch), "Mode":Mode.get(), "ClickButton":ClickButton.get()}
    with open (filename, 'w') as json_file:
        json.dump(settings, json_file)

#function to load file

def load_file(filename="settings.json"):
    global cps, keybind, Killswitch, Mode, ClickButton, sleeping, setsleeping
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        cps, keybind, Killswitch = parse_json(data)


        sleeping, setsleeping = calculate_sleeping(cps)
        CPS_label.config(text='Current CPS: {}'.format(cps))
        keybind_label.config(text='Activate Keybind: {}'.format(keybind))
        keybind_label_KS.config(text='Activate Killswitch Keybind: {}'.format(Killswitch))
        
        
        Mode.set(data["Mode"])
        Hold_Title.config(text=f"Mode: {Mode_list[Mode.get()]}")
        
        ClickButton.set(data["ClickButton"])
        ClickButton_Title.config(text=f"Click Button: {ClickButton_list[ClickButton.get()]}")
        print("load success") #debugging purposes
    except:
        print("load fail") #debugging purposes
        return 

def parse_json(data):
    cps = float(data["cps"])
    keybind = eval((data["keybind"]), {"Button": MouseButton, "Key": keyboard.Key})
    Killswitch = eval((data["Killswitch"]) , {"Key": keyboard.Key})

    if isinstance(keybind, str):
        keybind = keyboard.KeyCode.from_char(keybind) #keyboard is library(or file), keycode is class, from_char is class method 
    if isinstance(Killswitch, str):
        Killswitch = keyboard.KeyCode.from_char(Killswitch) #we need to use this function for normal character keys(that hasn't been transformed to keyboard objects yet, because they map character keys dynamically with from_char classmethod)

    return cps, keybind, Killswitch
    
# seperation

def clear():
    global cps
    
    entry.delete(0, END)
    cps = None
    CPS_label.config(text='Current CPS: {}'.format(cps))

#FOR KEYBINDS

def keybind_specific():
    global keybind_select
    if keybind_select == 'None':
        keybind_select = 'Keybind'
        threading.Thread(target=capture_keybind, daemon=True).start()

    


def killswitch_specific():
    global keybind_select
    if keybind_select == 'None':
        keybind_select = 'Killswitch'
        threading.Thread(target=capture_keybind, daemon=True).start()

    
    
#We cannot start multithread here immediately otherwise the system will crash since you are messing with window.mainloop()
#Basically we need to start both of the threads when we are already outside of the mainthread
def capture_keybind():
    global m_listener, k_listener, keybind_select
    if keybind_select == 'Keybind':
        keybind_label.config(text='Activate Keybind: Awaiting Input')
    elif keybind_select == 'Killswitch':
        keybind_label_KS.config(text='Activate Killswitch Keybind: Awaiting Input')
        
    m_listener = MouseListener(on_click=on_click_keybind, daemon=True)
    k_listener = KeyboardListener(on_press=on_press_keybind, daemon=True)
    m_listener.start()
    k_listener.start()
    m_listener.join()
    k_listener.join()

def on_click_keybind(x, y, button, pressed):
    global m_listener, k_listener, keybind, keybind_select, Killswitch
    invalid_list = [MouseButton.left,MouseButton.right, MouseButton.middle] #Ensure users can't set the autoclick buttons same as keybind
    if pressed and button not in invalid_list:
        if keybind_select == 'Keybind':
            keybind = button
            keybind_label.config(text='Activate Keybind: {}'.format(keybind))
            keybind_select = 'None'

            m_listener.stop()
            k_listener.stop()
            save_file()
            return False #only put False if you want to close the mouse.Listener
        elif keybind_select == 'Killswitch':

            keybind_label_KS.config(text='Activate Keybind: Mouse button cannot be accepted')
            keybind_select = 'None'

            m_listener.stop()
            k_listener.stop()
            save_file()
            return False #only put False if you want to close the mouse.Listener
    
def on_press_keybind(key):    
    global m_listener, k_listener, keybind, keybind_select, Killswitch 
    if keybind_select == 'Keybind':
        keybind = key
        keybind_label.config(text='Activate Keybind: {}'.format(keybind))
        keybind_select = 'None'

        m_listener.stop()
        k_listener.stop()
        save_file()
        return False #only put False if you want to close the keyboard.Listener
    elif keybind_select == 'Killswitch':
        Killswitch = key
        keybind_label_KS.config(text='Activate Keybind: {}'.format(Killswitch))
        keybind_select = 'None'

        m_listener.stop()
        k_listener.stop()
        save_file()
        return False #only put False if you want to close the keyboard.Listener

#FOR HOLD AND TOGGLE
def changeMode():

    Hold_Title.config(text=f"Mode: {Mode_list[Mode.get()]}")
    save_file()

#FOR CLICK BUTTON
def change_click():

    ClickButton_Title.config(text=f"Click Button: {ClickButton_list[ClickButton.get()]}")
    save_file()

#FOR ENDING
def close():
    print('sucess')
    KB_listener.stop()
    MO_listener.stop()
    window.destroy()
    sys.exit()


    

#CPS input
CPS_label = Label(window, text='Current CPS: {}'.format(cps))
CPS_label.pack(pady=5)

entry = Entry()
entry.pack(padx=5,pady=5)

button_frame = Frame(window)
button_frame.pack(pady=5)

submit = Button(button_frame, text="Submit", command=submit)
submit.pack(pady=5, padx=5, side=LEFT)

clear = Button(button_frame, text="Clear", command=clear)
clear.pack(pady=5, padx=5, side=LEFT)

#Keybind part
keybind_label = Label(window, text='Activate Keybind: {}'.format(keybind))
keybind_label.pack(pady=5)

keybind_button = Button(window, text='Reset Keybind', command=keybind_specific)
keybind_button.pack(pady=5)

#Kill switch
keybind_label_KS = Label(window, text='Activate Killswitch Keybind: {}'.format(Killswitch))
keybind_label_KS.pack(pady=5)

keybind_button_KS = Button(window, text='Reset Keybind', command=killswitch_specific)
keybind_button_KS.pack(pady=5)

#Hold/Toggle

Hold_Title = Label(window, text=f"Mode: {Mode}")
Hold_Title.pack(pady=5)
Mode = IntVar()
Mode_list = ["Hold", "Toggle"]
for x in range(len(Mode_list)):
    radiobutton_mode = Radiobutton(window, text=Mode_list[x], variable=Mode,
                                   value=x, padx=25, command=changeMode)
    radiobutton_mode.pack(anchor=W)



#Auto click button

ClickButton_Title = Label(window, text=f"Click Button: {ClickButton}")
ClickButton_Title.pack(pady=5)
ClickButton = IntVar()
ClickButton_list = ["left", "right", "middle"] #0 left, 1 right and 2 is middle
for y in range(len(ClickButton_list)):
    radiobutton_click = Radiobutton(window, text=ClickButton_list[y], variable=ClickButton,
                                   value=y, padx=25, command=change_click)
    radiobutton_click.pack(anchor=W)

#Autoclicking backend
mouse_controller = Controller()
def on_press_toggle(key):
    global activated, sleeping, keybind, setsleeping, Killswitch
    try:
        if key.char == Killswitch:
            close()
    except AttributeError:
        if key == Killswitch: #Users should be able to pick kill switch

            close()
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
    global activated, sleeping, keybind, setsleeping, Killswitch
    try:
        if (key.char).lower() == (keybind.char).lower():
            activated = True
            sleeping = setsleeping
            pass
    except AttributeError:
        if key == keybind:
            activated = True
        pass
    try:
        if (key.char).lower() == (Killswitch.char).lower():
            close()

    except AttributeError:
        if key == Killswitch:
            close()




def on_release_hold(key):
    global activated, keybind
    try:
        if (key.char).lower() == (keybind.char).lower():
            activated = False
    except AttributeError:
        if key == keybind:  #key.char doesn't work for special keys like ecs and f7 for those cases normal key == keybind works fine
            activated = False
        pass
    
def on_press_mousecon(x,y,button, pressed):
    global activated, keybind, sleeping, setsleeping
    if button == keybind:
        if Mode_list[Mode.get()] == 'Toggle':
            activated = not activated
            if not activated:
                sleeping = setsleeping
        elif Mode_list[Mode.get()] == 'Hold':
            if pressed:
                activated = True
                sleeping = setsleeping
            elif not pressed:
                activated = False


def perform_macro():
    global activated, sleeping, ClickButton
    Mouselist = [MouseButton.left, MouseButton.right, MouseButton.middle]

    while True:
        if activated:
            mouse_controller.click(Mouselist[ClickButton.get()], 1)  #we need to use clickbutton.get() because intvar is not a variable but an instance to get var we need to call it's classmethod
            while True:
               sleepingrand = np.random.laplace(sleeping, sleeping*0.2)  #CPS INSTANTANEOUS SPEED DISTRIBUTION
               if sleepingrand <= 4*sleeping and sleepingrand >= sleeping*0.3:
                   break
            time.sleep(sleeping)
            sleeping = random.uniform(sleeping*1.0005,sleeping*1.001) #CPS DECAY
        else:                           #Added this little part which drastically stabilises performance at high cps
            time.sleep(0.01)
            

threading.Thread(target=perform_macro, daemon=True).start()

window.protocol("WM_DELETE_WINDOW", close) #This tells python to call the close function to close program properly when user closes the macro's 


load_file() #Loads file duh

if Mode_list[Mode.get()] == 'Toggle':
    KB_listener = KeyboardListener(on_press=on_press_toggle)
    MO_listener = MouseListener(on_click=on_press_mousecon)

    KB_listener.start()
    MO_listener.start()

        
elif Mode_list[Mode.get()] == 'Hold':
    KB_listener = KeyboardListener(on_press=on_press_hold, on_release=on_release_hold)
    MO_listener = MouseListener(on_click=on_press_mousecon)


    KB_listener.start()
    MO_listener.start()

    


window.mainloop()

KB_listener.join()
MO_listener.join()


#END


