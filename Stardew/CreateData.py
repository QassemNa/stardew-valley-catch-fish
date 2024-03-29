import numpy as np
import os


file_name = "data/training_data.npy"
file_name2 = "data/target_data.npy"
file_name3 = "data/caught_data.npy"


def get_data():

    if os.path.isfile(file_name):
        print('File exists, loading previous data!')
        image_data = list(np.load(file_name, allow_pickle=True))
        targets = list(np.load(file_name2, allow_pickle=True))
        num_caught = list(np.load(file_name3, allow_pickle=True))
    else:
        print('File does not exist, starting fresh!')
        image_data = []
        targets = []
        num_caught = [0]
    return image_data, targets, num_caught


def save_data(image_data, targets, num_caught):
    np.save(file_name, image_data)
    np.save(file_name2, targets)
    np.save(file_name3, num_caught)


#image_data, targets = get_data()
"""
while True:
    keys = key_check()
    print("waiting press B to start")
    if keys == "B":
        print("Starting")
        break


time.sleep(2)
count = 0
while True:
    count +=1
    last_time = time.time()
    image = grab_screen(region=(805, 255, 830, 805)) # region=(50, 100, 799, 449)bb
    image = cv2.cvtColor(image, cv2.IMREAD_COLOR) # b

    image = cv2.Canny(image, threshold1=119, threshold2=250)

    image = cv2.resize(image, (25, 550))

    # Debug line to show image
    #cv2.imshow("AI Peak", image)
    #cv2.waitKey(0)

    # Convert to numpy array
    image = np.array(image)
    image_data.append(image)

    keys = key_check()
    targets.append(keys)
    if keys == "H":
        break

    print('loop took {} seconds'.format(time.time()-last_time))

save_data(image_data, targets)
"""