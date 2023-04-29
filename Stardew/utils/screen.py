import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api
from mss.base import MSSBase


def grab_screen(region=None):
    hwin = win32gui.GetDesktopWindow()

    if region:
        left, top, x2, y2 = region
        width = x2 - left + 1
        height = y2 - top + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)

    # cv2.imwrite("imageFULL.png", img)
    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)


def main_screen(screen_shot, just_reel=False):
    if just_reel:
        dimensions = {
            'left': 800,
            'top': 30,
            'width': 219,
            'height': 620
        }
    else:
        dimensions = {
            'left': 0,
            'top': 30,
            'width': 1280,
            'height': 720
        }
    scr = screen_shot.grab(dimensions)
    img = np.array(scr)
    return cv2.cvtColor(img, cv2.IMREAD_COLOR)


def fix_image(img):
    s = max(img.shape[0:2])
    f = np.zeros((s, s, 3), np.uint8)
    ax, ay = (s - img.shape[1]) // 2, (s - img.shape[0]) // 2
    f[ay:img.shape[0] + ay, ax:ax + img.shape[1]] = img
    # f = cv2.Canny(f, threshold1=119, threshold2=250)
    image = cv2.resize(f, (224, 224))
    return image
