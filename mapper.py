
from inputs import devices
from inputs import get_gamepad
from threading import Thread
from time import sleep
import pyautogui
import queue
import time
import numpy as np


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class ThreadedInputs:
    NOMATCH = 'No Match'

    def __init__(self):
        # Initialise gamepad command dictionary.
        # Add gamepad commands using the append method before executing the start method.
        self.gamepadInputs = {}
        self.lastEventCode = self.NOMATCH
        # Initialise the thread status flag
        self.stopped = False
        self.q = queue.LifoQueue()

    def start(self):
        # Start the thread to poll gamepad event updates
        t = Thread(target=self.gamepad_update, args=())
        t.daemon = True
        t.start()

    def gamepad_update(self):
        while True:
            # Should the thread exit?
            if self.stopped:
                return
            # Code execution stops at the following line until a gamepad event occurs.
            events = get_gamepad()
            for event in events:
                event_test = self.gamepadInputs.get(event.code, self.NOMATCH)
                if event_test != self.NOMATCH:
                    self.gamepadInputs[event.code] = event.state
                    self.lastEventCode = event.code
                    self.q.put(event.code)

    def read(self):
        # Return the latest command from gamepad event
        if not self.q.empty():
            newCommand = self.q.get()
            while not self.q.empty():
                trashBin = self.q.get()

            return newCommand, self.gamepadInputs[newCommand]
        else:
            return self.NOMATCH, 0

    def stop(self):
        # Stop the game pad thread
        self.stopped = True

    def append_command(self, newCommand, newValue):
        # Add new controller command to the list
        if newCommand not in self.gamepadInputs:
            self.gamepadInputs[newCommand] = newValue
        else:
            print('New command already exists')

    def delete_command(self, commandKey):
        # Remove controller command from list
        if commandKey in self.gamepadInputs:
            del self.gamepadInputs[commandKey]
        else:
            print('No command to delete')

    def command_value(self, commandKey):
        # Get command value
        if commandKey in self.gamepadInputs:
            return self.gamepadInputs[commandKey]
        else:
            return None

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

    # start multiprocessing

    # for device in devices:
    #     print(devices)

    #printing some random stuff?
    print(devices.gamepads)
    print(devices.keyboards)
    print(devices.mice)
    print(devices.other_devices)

    #random deadzone that i just came up with. if the value is within this radius of zero, dont do anything.
    deadzone = 7000;

    #mouse sentivity
    xSensitivity = 50;
    ySensitivity = 50;

    gamepad = ThreadedInputs()

    for input in gamepadInputs:
        gamepad.append_command(input, gamepadInputs[input])

    while 1:
        events = get_gamepad()
        for event in events:
            #event.ev_type, event.code, event.state
            # print(event.code, event.state)
            if (event.state >= deadzone or event.state <= -deadzone):
                if (event.code == "ABS_X"):
                    print(event.code, event.state)
                    pyautogui.moveRel(np.sign(int(event.state)) * 50, 0, duration=0)
                    print("\tHORIZONTAL MOVEMENT")
                if (event.code == "ABS_Y"):
                    print(event.code, event.state)
                    pyautogui.moveRel(0, -np.sign(int(event.state)) * 50, duration=0)
                    print("\tVERTICAL MOVEMENT")

def main():
    print_hi("ijwauhkddhasjkhdjkas")

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
	""" This is executed when run from the command line """
	main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
