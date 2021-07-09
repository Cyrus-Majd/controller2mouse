
from inputs import devices
from inputs import get_gamepad
from time import sleep
import threading
import pyautogui
import numpy as np
import pandas as pds

## Thread to check if user wants to quit program.
class ProgramManager(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.quitFlag = False
    
    def readQuitFlag(self):
        while(self.quitFlag == False):
            value = input("Type 'quit' to quit.")
            if (value == "quit"):
                self.quitFlag = True
            else:
                print("Unrecognized command. Try again.")

    def run(self):
        self.readQuitFlag()

## Thread to contstantly read input from controller.
class Controller(threading.Thread):

    # Constructor.
    def __init__(self, xSensitivity, ySensitivity, deadzone):
        self.xMotion = 0
        self.yMotion = 0
        self.outOfDeadzone = False

        self.livingFlag = True
        self.xSensitivity = xSensitivity
        self.ySensitivity = ySensitivity
        self.deadzone = deadzone
        threading.Thread.__init__(self)
        self.threadLock = threading.Lock()

    # Method to read in inputs from controller.
    def readInputs(self):
        # DEBUG: Connected devices.
        for device in devices:
            print(devices)

        # DEBUG: Device details.
        print(devices.gamepads)
        print(devices.keyboards)
        print(devices.mice)
        print(devices.other_devices)

        while (self.livingFlag):
            events = get_gamepad()
            for event in events:
                if (event.state >= self.deadzone or event.state <= -self.deadzone):
                    self.outOfDeadzone = True
                    if (event.code == "ABS_X"):
                        print(event.code, event.state)
                        pyautogui.moveRel(np.sign(int(event.state)) * self.xSensitivity, 0, duration=0)
                        print("\tHORIZONTAL MOVEMENT")
                    if (event.code == "ABS_Y"):
                        print(event.code, event.state)
                        pyautogui.moveRel(0, -np.sign(int(event.state)) * self.ySensitivity, duration=0)
                        print("\tVERTICAL MOVEMENT")
                    self.outOfDeadzone = False
    
    # Default threading entry method.
    def run(self):
        self.readInputs()

# Main method.
def main():
    controllerObj = Controller(10, 10, 7000)
    controllerObj.start()

    sleep(1)

    programManagerObj = ProgramManager()
    programManagerObj.start()

    # Loop updates inputs from controller as long as the quit flag has not been raised.
    while(programManagerObj.quitFlag == False):
        sleep(1)
    
    controllerObj.livingFlag = False
    controllerObj.join()

if __name__ == "__main__":
	""" This is executed when run from the command line """
	main()
