import numpy as np
import cv2
import time
import os

file_name = "data/training_data.npy"
file_name2 = "data/target_data.npy"
file_name3 = "data/caught_data.npy"

path_C = "data/Stardew_images/C/C"
path_Nothing = "data/Stardew_images/Nothing/N"

image_data = list(np.load(file_name, allow_pickle=True))
targets = list(np.load(file_name2, allow_pickle=True))
num_caught = list(np.load(file_name3, allow_pickle=True))

counter = 0
for img, key in zip(image_data, targets):
    counter += 1
    # if counter >=1200:
    #    break
    if key == 'C':
        print("C!")
        cv2.imwrite(path_C + str(counter) + ".png", img)
    elif key == 'O':
        print("NOTHING")
        cv2.imwrite(path_Nothing + str(counter) + ".png", img)
