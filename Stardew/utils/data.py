import cv2
import numpy as np

from Stardew.CreateData import save_data
from Stardew.utils.screen import fix_image


def collect_data(images, image_data, targets, num_caught):
    images = images[:-15]

    for image in images:
        pass
        img = fix_image(image[0])

        cv2.imwrite("data/images/" + str(image[2]) + ".png", img=img)
        img = np.array(img)
        image_data.append(img)
        targets.append(image[1])
        num_caught[0] += 1
    save_data(image_data, targets, num_caught)
