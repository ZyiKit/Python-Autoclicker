from tkinter import *

window = Tk()

window.geometry("350x450")
window.title("Python Autoclicker")

# Ensure the software doesn't crash when image doesn't load
try:
    icon = PhotoImage(file='python_logo.png')
    window.iconphoto(True, icon)
except Exception:
    pass

global cps
cps = None
keybind = None
Killswitch = None
Mode = None
ClickButton = None


#FOR CPS INPUT
def submit():
    cps = entry.get()
    CPS_label.config(text='Current CPS: {}'.format(cps))

def clear():
    entry.delete(0, END)
    cps = None
    CPS_label.config(text='Current CPS: {}'.format(cps))

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

keybind_button = Button(window, text='Reset Keybind')
keybind_button.pack(pady=5)

#Kill switch
keybind_label = Label(window, text='Activate Killswitch Keybind: {}'.format(Killswitch))
keybind_label.pack(pady=5)

keybind_button = Button(window, text='Reset Keybind')
keybind_button.pack(pady=5)

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






#END

window.mainloop()
