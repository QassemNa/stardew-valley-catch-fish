# direct inputs
# source to this solution and code:
# http://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
# http://www.gamespp.com/directx/directInputKeyboardScanCodes.html

import ctypes
import time
import datetime


SendInput = ctypes.windll.user32.SendInput
W = 0x11
A = 0x1E
S = 0x1F
D = 0x20
Space = 0x39
num1=0x4F
num2=0x50
pic=[0x02,0x03,0x04]


# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

if __name__ == '__main__':
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=1)
    time.sleep(3)
    currentpic=pic[0]
    count=0
    i=0
    while True:
        if datetime.datetime.now() >= endTime - datetime.timedelta(seconds=230):
            count=1
            currentpic=pic[count]
            PressKey(currentpic)
            time.sleep(0.1)
            ReleaseKey(currentpic)
        if(i>=16):
            PressKey(0x0A)
            time.sleep(0.2)
            ReleaseKey(0x0A)
            PressKey(num2)
            time.sleep(0.2)
            ReleaseKey(num2)
            PressKey(currentpic)
            time.sleep(0.1)
            ReleaseKey(currentpic)
            i=0
        if datetime.datetime.now() >= endTime:
            break
        i=i+1
        PressKey(W)
        time.sleep(0.3)
        ReleaseKey(W)
        PressKey(num1)
        time.sleep(1.38)
        #time.sleep(0.8)#time between two blocks
        #ReleaseKey(num0)
        #time.sleep(0.5)
        #PressKey(num0)
        #time.sleep(0.8)#time between two blocks
        ReleaseKey(num1)


#for two blocks we need a total of 1:32
#18 blocks then light
#


