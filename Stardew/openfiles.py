import numpy as np
import cv2
path = 'data/training_data.npy'
training = list(np.load(path, allow_pickle=True))
print(len(training))
"""
for train in training:
    for t in train:
            print(t)
"""
#cv2.imshow("AI Peak", training[223])
#cv2.waitKey(0)

#a = []
#a.append(33)
#num_caught = np.save("data/caught_data.npy", a)

num_caught = list(np.load("data/caught_data.npy", allow_pickle=True))
print(num_caught)
