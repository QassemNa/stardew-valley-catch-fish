# direct inputs
# source to this solution and code:
# http://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
# http://www.gamespp.com/directx/directInputKeyboardScanCodes.html

import ctypes
import time
import datetime
from Stardew.utils.Controls import ReleaseKey, PressKey

SendInput = ctypes.windll.user32.SendInput
W = 0x11
A = 0x1E
S = 0x1F
D = 0x20
X = 0x2D
C = 0x2E
Space = 0x39
num1 = 0x4F
num2 = 0x50


def LeaveRoom():
    time.sleep(1.2)
    PressKey(A)
    time.sleep(1.2)
    ReleaseKey(A)
    PressKey(S)
    time.sleep(0.5)
    ReleaseKey(S)


def LeaveFarm():
    time.sleep(1.2)
    PressKey(S)
    time.sleep(0.5)
    ReleaseKey(S)
    PressKey(D)
    time.sleep(3.2)
    ReleaseKey(D)


def LeaveStation():
    time.sleep(1.2)
    PressKey(D)
    time.sleep(7)
    ReleaseKey(D)


def LeaveTown():
    time.sleep(1.2)
    PressKey(D)
    time.sleep(5.4)
    ReleaseKey(D)
    PressKey(S)
    time.sleep(4)
    ReleaseKey(S)
    PressKey(D)
    time.sleep(5.35)
    ReleaseKey(D)
    PressKey(S)
    time.sleep(7.2)
    ReleaseKey(S)


def ToSea():
    LeaveRoom()
    LeaveFarm()
    LeaveStation()
    LeaveTown()
    time.sleep(1.2)
    PressKey(S)
    time.sleep(1.75)
    ReleaseKey(S)
    PressKey(A)
    time.sleep(2.75)
    ReleaseKey(A)
    PressKey(S)
    time.sleep(4)
    ReleaseKey(S)
    PressKey(A)
    time.sleep(0.3)
    ReleaseKey(A)


def Fish():
    PressKey(num1)
    time.sleep(0.1)
    ReleaseKey(num1)
    PressKey()


if __name__ == '__main__':
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=1)
    ToSea()

# for two blocks we need a total of 1:32
# 18 blocks then light
#
