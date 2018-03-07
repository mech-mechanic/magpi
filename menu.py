# import evdev
from evdev import InputDevice, categorize, ecodes
import os
import time

from Watch import WatchFace

# create jpad object 
jpad = InputDevice('/dev/input/event0')

# create watch face object
face = WatchFace()

# Method test
face.stats 

# print device info
print(jpad)

# polling loop
for event in jpad.read_loop():
    if event.type == ecodes.EV_KEY:
        if event.code == 56:
            if categorize(event).keystate == 1:
                    os.system('python time.py')
                    os.system('python clear.py')


