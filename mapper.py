
from inputs import devices
from inputs import get_gamepad
from time import sleep
import threading
import pyautogui
import numpy as np
import pandas as pds



## Threaded class.
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
                        # pyautogui.moveRel(np.sign(int(event.state)) * self.xSensitivity, 0, duration=0)
                        print("\tHORIZONTAL MOVEMENT")
                    if (event.code == "ABS_Y"):
                        print(event.code, event.state)
                        # pyautogui.moveRel(0, -np.sign(int(event.state)) * self.ySensitivity, duration=0)
                        print("\tVERTICAL MOVEMENT")
                    self.outOfDeadzone = False
    
    # Default threading entry method.
    def run(self):
        self.readInputs()

# Main method.
def main():
    obj = Controller(10, 10, 7000)
    obj.start()

    # Loop which checks for program ending flag AND updates mouse state/etc from inputs.
    while(obj.livingFlag):

        

        

    obj.join()

if __name__ == "__main__":
	""" This is executed when run from the command line """
	main()
