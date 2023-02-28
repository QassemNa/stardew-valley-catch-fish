import random
import time

from utils.getkeys import key_check
import pydirectinput
import keyboard
import time
import cv2
from utils.screen import grab_screen
from utils.Controls import PressKey, ReleaseKey
from fastai.vision.all import *


def label_func(x): return x.parent.name

model_file = "data/model/export3.pkl"
learn_inf = load_learner(model_file)
print("loaded learner")

# Sleep time after actions
sleepy = 0.1

# Wait for me to push B to start.
time.sleep(sleepy)


# Hold down W no matter what!

# Randomly pick action then sleep.
# 0 do nothing release everything ( except W )
# 1 hold left
# 2 hold right
# 3 Press Jump
def predict():
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

    # action = random.randint(0,3)
    if action == "Nothing":
        # print("Doing nothing....")
        keyboard.release("c")
        time.sleep(sleepy)

    elif action == "C":
        print(f"Reel! - {result[1]}")
        keyboard.press("c")
        time.sleep(sleepy)


"""
while True:

    

    # End simulation by hitting h
    keys = key_check()
    if keys == "H":
        break

"""
