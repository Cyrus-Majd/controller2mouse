from __future__ import division
from inputs import devices
from inputs import get_gamepad
from time import sleep
import math
import threading
import pyautogui
import numpy as np
import pandas as pds
import autopy

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
        self.xAmplitude = 0
        self.yAmplitude = 0

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
                if (event.state >= self.deadzone or event.state <= -self.deadzone):     # beyond deadzone
                    ## MIN/MAX X VALUE: -32768 --> 32767
                    ## MIN/MAX Y VALUE: 32767 --> -32768
                    if (event.code == "ABS_X"):
                        # print(event.code, event.state, math.fabs(int(event.state) / 32767))
                        self.xMotion = np.sign(int(event.state)) * self.xSensitivity
                        self.xAmplitude = math.fabs(int(event.state) / 32768)
                        # print("\tHORIZONTAL MOVEMENT, AMP:", self.xAmplitude)
                    if (event.code == "ABS_Y"):
                        # print(event.code, event.state, math.fabs(int(event.state) / 32767))
                        self.yMotion = -np.sign(int(event.state)) * self.ySensitivity
                        self.yAmplitude = math.fabs(int(event.state) / 32768)
                        # print("\tVERTICAL MOVEMENT, AMP:", self.yAmplitude)
                # elif (event.state <= self.deadzone and event.state >= -self.deadzone):    # within deadzone
                    # self.xAmplitude = 0
                    # self.yAmplitude = 0
                #     print("IN CENTER, AMPS:", self.xAmplitude, self.yAmplitude)
                # else:
                #     print("NO MOVEMENT, AMPS:", self.xAmplitude, self.yAmplitude)
    
    # Default threading entry method.
    def run(self):
        self.readInputs()

def moveCursor(xOne, xTwo, yOne, yTwo):
    pyautogui.PAUSE = 0.01
    pyautogui.MINIMUM_DURATION = 0.1
    pyautogui.moveTo(xTwo, yTwo, duration = .2, tween = pyautogui.linear)

def calculatePath(xMotion, yMotion, xAmp, yAmp):
    xPosition = pyautogui.position()[0]
    yPosition = pyautogui.position()[1]

    xDisplacement = int(xMotion * xAmp)
    yDisplacement = int(yMotion * yAmp)

    xDestination = xPosition + xDisplacement
    yDestination = yPosition + yDisplacement

    sleep(1)

    print(xPosition, yPosition, xDestination, yDestination)

    moveCursor(xPosition, xDestination, yPosition, yDestination)

# Main method.
def main():
    pyautogui.FAILSAFE = False

    # calculatePath(100, -100, 3, 3)

    controllerObj = Controller(100, 100, 0)
    controllerObj.start()

    sleep(1)

    programManagerObj = ProgramManager()
    programManagerObj.start()

    # Loop updates inputs from controller as long as the quit flag has not been raised.
    while(programManagerObj.quitFlag == False):
        if (controllerObj.xAmplitude > .05 or controllerObj.yAmplitude > .05):
            # print("\tXMOTION: ", controllerObj.xMotion, "YMOTION:", controllerObj.yMotion, "AMPx:", controllerObj.xAmplitude, "AMPy:", controllerObj.yAmplitude)
            # moveCursor(calculatePath(controllerObj.xMotion, controllerObj.yMotion, controllerObj.xAmplitude, controllerObj.yAmplitude))
            pyautogui.moveRel(controllerObj.xMotion * controllerObj.xAmplitude, controllerObj.yMotion * controllerObj.yAmplitude, duration=.1)  ## MOVE X VALUE
            # pyautogui.moveRel(0, controllerObj.yMotion * controllerObj.yAmplitude, duration=.15) ## MOVE Y VALUE
    
    controllerObj.livingFlag = False
    controllerObj.join()

if __name__ == "__main__":
	""" This is executed when run from the command line """
	main()
