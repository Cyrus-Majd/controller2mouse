
from inputs import devices
from inputs import get_gamepad


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

    # for device in devices:
    #     print(devices)

    #printing some random stuff?
    print(devices.gamepads)
    print(devices.keyboards)
    print(devices.mice)
    print(devices.other_devices)

    #random deadzone that i just came up with. if the value is within this radius of zero, dont do anything.
    deadzone = 7000;

    while 1:
        events = get_gamepad()
        for event in events:
            #event.ev_type, event.code, event.state
            # print(event.code, event.state)
            if (event.state >= deadzone or event.state <= -deadzone):
                if (event.code == "ABS_X"):
                    print(event.code, event.state)
                    print("\tWE DID IT")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
