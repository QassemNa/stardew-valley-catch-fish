import time

from timeit import default_timer as timer

import keyboard
import mss as mss
import numpy as np
import cv2
from mss.base import MSSBase

from utils.Controls import PressKey, ReleaseKey

from utils.screen import grab_screen, main_screen, fix_image
from utils.getkeys import key_check
from CreateData import get_data, save_data

from fastai.vision.all import *


def label_func(x): return x.parent.name


model_file = "data/model/export2.pkl"
learn_inf = load_learner(fname=model_file)
print("loaded learner")

sleepy = 0.1

# Wait for me to push B to start.
time.sleep(sleepy)

# Hold down W no matter what!

# Randomly pick action then sleep.
# 0 do nothing release everything ( except W )
# 1 hold left
# 2 hold right
# 3 Press Jump

W = 0x11
A = 0x1E
S = 0x1F
D = 0x20
X = 0x2D
C = 0x2E
Space = 0x39
num1 = 0x4F
num2 = 0x50

SCT: MSSBase = mss.mss()

import os, os.path


# simple version for working with CWD
def predict():
    start = timer()
    image = grab_screen(region=(791, 42, 845, 616))  # 805, 60, 830, 605
    image = cv2.cvtColor(image, cv2.IMREAD_COLOR)

    s = max(image.shape[0:2])
    f = np.zeros((s, s, 3), np.uint8)
    ax, ay = (s - image.shape[1]) // 2, (s - image.shape[0]) // 2
    f[ay:image.shape[0] + ay, ax:ax + image.shape[1]] = image
    # f = cv2.Canny(f, threshold1=119, threshold2=250)
    image = cv2.resize(f, (224, 224))

    # cv2.imshow("Fall", image)
    # cv2.waitKey(1)
    start_time = time.time()
    result = learn_inf.predict(image)
    action = result[0]
    # print(result[2][0].item(), result[2][1].item(), result[2][2].item(), result[2][3].item())
    end = timer()
    # action = random.randint(0,3)
    print(action)
    if action == "Nothing":
        print(f"Nothing! - {result[1]}", end - start)
        ReleaseKey(C)
        time.sleep(sleepy)

    elif action == "C":
        print(f"Reel! - {result[1]}", end - start)
        PressKey(C)
        time.sleep(sleepy)


def isCatchingFish():
    fish = False

    color = cv2.cvtColor(main_screen(screen_shot=SCT), cv2.IMREAD_COLOR)

    result_Caught_Something = cv2.matchTemplate(color, Caught_Something, cv2.TM_CCOEFF_NORMED)
    _, max_val_Caught_Something, _, max_loc_Caught_Something = cv2.minMaxLoc(result_Caught_Something)

    result_Idle = cv2.matchTemplate(color, Idle, cv2.TM_CCOEFF_NORMED)
    _, max_val_Idle, _, max_loc_Idle = cv2.minMaxLoc(result_Idle)

    # result_End_Reel = cv2.matchTemplate(color, End_Reel, cv2.TM_CCOEFF_NORMED)
    # _, max_val_End_Reel, _, max_loc_End_Reel = cv2.minMaxLoc(result_End_Reel)

    # if max_val_End_Reel >= 0.85:
    #    print("END OF REEL")
    if max_val_Caught_Something >= 0.85:

        result_Caught_Fish = cv2.matchTemplate(color, Caught_Fish, cv2.TM_CCOEFF_NORMED)
        _, max_val_Caught_Fish, _, max_loc_Caught_Fish = cv2.minMaxLoc(result_Caught_Fish)

        if max_val_Caught_Fish >= 0.85:
            fish = True
        else:
            fish = False
        return False, fish
    elif max_val_Idle >= 0.85:
        return False, False
    else:
        return True, fish


count, counter = 0, 0
time.sleep(2)
file = os.listdir('data/images')
for pic in file:
    if count < int(pic[:-4]):
        count = int(pic[:-4])

caught = cv2.imread('Screenshots/Caught.png', cv2.IMREAD_UNCHANGED)
fishing = cv2.imread('Screenshots/Fishing.png', cv2.IMREAD_UNCHANGED)
Idle = cv2.imread('Screenshots/Idle.png', cv2.IMREAD_UNCHANGED)
Caught_Fish = cv2.imread('Screenshots/Caught_Fish.png', cv2.IMREAD_UNCHANGED)
Caught_Something = cv2.imread('Screenshots/Caught_Something.png', cv2.IMREAD_UNCHANGED)
End_Reel = cv2.imread('Screenshots/End_Reel.png', cv2.IMREAD_UNCHANGED)

# Caught_Hit_mask = cv2.imread('Screenshots/HIT_mask2.png', cv2.IMREAD_COLOR )
# Caught_Hit = cv2.imread('Screenshots/HIT.png', cv2.IMREAD_COLOR )


# cv2.TM_SQDIFF or cv2.TM_CCORR_NORMED http://docs.opencv.org/2.4/doc/tutorials/imgproc/histograms/template_matching
# /template_matching.html#which-are-the-matching-methods-available-in-opencv method = cv2.TM_CCOEFF_NORMED  # R(x,
# y) = \sum _{x',y'} (T(x',y')-I(x+x',y+y'))^2 (essentially, sum of squared differences)


while 1:

    color = cv2.cvtColor(main_screen(screen_shot=SCT), cv2.IMREAD_COLOR)
    start = timer()

    result_caught = cv2.matchTemplate(color, caught, cv2.TM_CCOEFF_NORMED)
    result_Idle = cv2.matchTemplate(color, Idle, cv2.TM_CCOEFF_NORMED)

    _, max_val_caught, _, max_loc_caught = cv2.minMaxLoc(result_caught)
    _, max_val_Idle, _, max_loc_Idle = cv2.minMaxLoc(result_Idle)

    end = timer()
    if max_val_caught >= 0.8:
        PressKey(C)
        time.sleep(0.1)
        ReleaseKey(C)
        image_data, targets, num_caught = get_data()
        time.sleep(2)
        images = []
        while 1:
            start = timer()
            isfishing = isCatchingFish()
            if not isfishing[0]:
                break
            count += 1
            last_time = time.time()
            predict()
            """
            these two lines are for collecting data
            image = grab_screen(region=(791, 42, 845, 616))  # 805, 60, 830, 605
            image = cv2.cvtColor(image, cv2.IMREAD_COLOR)  # b
            keys = key_check()
            images.append([image, keys, count])
            end = timer()
            #print(count, ": Key pressed is", keys, "\nIt took", end - start, "to run this loop")
            """
        if isfishing[1]:
            collect_data(images)
            count = int(count)
            print("You Caught a FISH !!!!!")
        else:
            if len(images) >= 1:
                count = images[0][2]
            print("Fish was not caught")

        PressKey(C)
        time.sleep(0.1)
        ReleaseKey(C)

    print(end - start, max_val_caught, max_val_Idle, counter)  # max_val_End_Reel , max_val_Caught_Fish max_val_fishing,
    counter += 1
    # cv2.rectangle(color, max_loc_caught, (max_loc_caught[0]+ 20, max_loc_caught[1]+50), (0,255,0), 5)
    # cv2.rectangle(color, max_loc_fishing, (max_loc_fishing[0] + 20, max_loc_fishing[1] + 50), (255, 0, 0), 5)
    # cv2.imshow("input", color)
    # cv2.waitKey(0)

    if max_val_Idle > 0.70:
        PressKey(num1)
        time.sleep(0.1)
        ReleaseKey(num1)

        PressKey(C)
        time.sleep(1)
        ReleaseKey(C)

    # result_fishing = cv2.matchTemplate(color, fishing, cv2.TM_CCOEFF_NORMED)
    # result_Caught_Fish = cv2.matchTemplate(color, Caught_Fish, cv2.TM_CCOEFF_NORMED)
    # result_Caught_Something = cv2.matchTemplate(color, Caught_Something, cv2.TM_CCOEFF_NORMED)
    # result_End_Reel = cv2.matchTemplate(color, End_Reel, cv2.TM_CCOEFF_NORMED)
    # result_Caught_Hit = cv2.matchTemplate(color, Caught_Hit, cv2.TM_CCORR_NORMED, None, Caught_Hit_mask)

    # _, max_val_fishing, _, max_loc_fishing = cv2.minMaxLoc(result_fishing)
    # _, max_val_Caught_Something, _, max_loc_Caught_Something = cv2.minMaxLoc(result_Caught_Something)
    # _, max_val_Caught_Fish, _, max_loc_Caught_Fish = cv2.minMaxLoc(result_Caught_Fish)
    # _, max_val_End_Reel, _, max_loc_End_Reel = cv2.minMaxLoc(result_End_Reel)
    # _, max_val_Caught_Hit, _, max_loc_Caught_Hit = cv2.minMaxLoc(result_Caught_Hit)
"""
Thoughts:
    1- discard images since we only have a limited variables
    2- variables are:
        A- Position of fish
        B- Position of Bar
        C- current reel state
        D- Distance from bar to fish
        R- distance the bar to either edge
        F- Size of bar
        G- is Reeling
        G- Bar Transparency; Not sure why
        H- 
    3- See how they made it in the other game
"""
