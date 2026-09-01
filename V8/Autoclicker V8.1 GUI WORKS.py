from tkinter import *
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener, Button as MouseButton, Controller
from pynput import keyboard
import threading
import time
import random
import numpy as np

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


cps = None
keybind = None
Killswitch = None
Mode = None
ClickButton = None
keybind_select = 'None'


#FOR CPS INPUT
def submit():
    cps = entry.get()
    CPS_label.config(text='Current CPS: {}'.format(cps))

def clear():
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
            return False #only put False if you want to close the mouse.Listener
        elif keybind_select == 'Killswitch':
            Killswitch = button
            keybind_label_KS.config(text='Activate Keybind: {}'.format(Killswitch))
            keybind_select = 'None'

            m_listener.stop()
            k_listener.stop()
            return False #only put False if you want to close the mouse.Listener
    
def on_press_keybind(key):    
    global m_listener, k_listener, keybind, keybind_select, Killswitch 
    if keybind_select == 'Keybind':
        keybind = key
        keybind_label.config(text='Activate Keybind: {}'.format(keybind))
        keybind_select = 'None'

        m_listener.stop()
        k_listener.stop()
        return False #only put False if you want to close the keyboard.Listener
    elif keybind_select == 'Killswitch':
        Killswitch = key
        keybind_label_KS.config(text='Activate Keybind: {}'.format(Killswitch))
        keybind_select = 'None'

        m_listener.stop()
        k_listener.stop()
        return False #only put False if you want to close the keyboard.Listener

#FOR HOLD AND TOGGLE
def changeMode():

    Hold_Title.config(text=f"Mode: {Mode_list[Mode.get()]}")

#FOR CLICK BUTTON
def change_click():

    ClickButton_Title.config(text=f"Click Button: {ClickButton_list[ClickButton.get()]}")
    
    

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
ClickButton_list = ["left", "right", "middle"]
for y in range(len(ClickButton_list)):
    radiobutton_click = Radiobutton(window, text=ClickButton_list[y], variable=ClickButton,
                                   value=y, padx=25, command=change_click)
    radiobutton_click.pack(anchor=W)




window.mainloop()


#END


