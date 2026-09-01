from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener, Button, Controller


captured_button = None


def on_click_keybind(x, y, button, pressed):
    global captured_button
    if pressed:
 
        captured_button = button
        print(f"Captured button inside function: {captured_button}")

        m_listener.stop()
        k_listener.stop()
        return False #only put False if you want to close the mouse.Listener


    
def on_press_keybind(key):
    global captured_button

    captured_button = key
    print(f"Captured button inside function: {captured_button}")

    m_listener.stop()
    k_listener.stop()
    return False #only put False if you want to close the keyboard.Listener



    
print("Waiting for an input.. (Any button other than left, right and middle mouse button)")

m_listener = MouseListener(on_click=on_click_keybind, daemon=True)
k_listener = KeyboardListener(on_press=on_press_keybind, daemon=True)

m_listener.start()
k_listener.start()

m_listener.join()
k_listener.join()

