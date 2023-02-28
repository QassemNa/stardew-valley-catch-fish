import time
import threading
from pynput.mouse import Button, Controller as mouseController
from pynput.keyboard import Listener, KeyCode, Controller as KeyController,Key

delay = 0.6
button = Button.left
start_stop_key = KeyCode(char='z')
exit_key = KeyCode(char='r')
w=KeyCode(char='w')


class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.ctr = 0
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:

                mouse.press(button)
                time.sleep(1)
                keyboard.press(w)
                mouse.release(button)


mouse = mouseController()
keyboard = KeyController()
click_thread = ClickMouse(delay, button)
click_thread.start()


def on_press(key):
    if key == start_stop_key:
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()
    elif key == exit_key:
        click_thread.exit()
        listener.stop()


with Listener(on_press=on_press) as listener:
    listener.join()
