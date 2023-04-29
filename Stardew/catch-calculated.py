import time
from cv2 import cv2
import numpy as np
import mss

from utils.screen import grab_screen, main_screen

SCT = mss.mss()
sleepy = 0.01


# cv2.imshow("AI Peak", main_screen())
# cv2.waitKey(0)
# image = grab_screen(region=(805, 255, 830, 805))  # region=(50, 100, 799, 449)bb
# img = cv2.imread("data/images/3.png")
DATA_NEEDED = []
while 1:

    # frame = cv2.imread("Screenshots/Screenshot_3.png")

    frame = main_screen(screen_shot=SCT)
    hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blue_lower = np.array([80, 150, 0], np.uint8)
    blue_upper = np.array([99, 255, 255], np.uint8)
    blue_mask = cv2.inRange(hsvframe, blue_lower, blue_upper)

    green_lower = np.array([40, 40, 40], np.uint8)
    green_upper = np.array([90, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsvframe, green_lower, green_upper)

    kernal = np.ones((5, 5), "uint8")

    blue_mask = cv2.dilate(blue_mask, kernal)
    res_blue = cv2.bitwise_and(frame, frame, mask=blue_mask)

    green_mask = cv2.dilate(green_mask, kernal)
    res_green = cv2.bitwise_and(frame, frame, mask=green_mask)

    # cv2.imshow("main", res_green)
    # cv2.waitKey(0)
    countours = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

    for contour in countours:
        area2 = cv2.contourArea(contour)
        if 950 > area2 > 200:
            x1, y1, w1, h1 = cv2.boundingRect(contour)
            frame_red = cv2.rectangle(
                frame, (x1, y1), (x1 + w1, y1 + h1), (0, 34, 255), 2
            )
            x_red2 = int(x1 + w1 / 2)  # x coordinate of fish
            y_red2 = int(y1 + h1 / 2)  # y coordinate of fish
            cv2.circle(frame, (x_red2, y_red2), 3, (0, 34, 255), -1)
            cv2.putText(
                frame,
                "hook",
                (x1 + w1, y1 + h1),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 34, 255),
            )

            try:
                distance2 = int(np.sqrt((x_red2 - x_green) ** 2 + (y_red2 - y_green) ** 2))
                print("Fish position:", y_red2, "Hook position:", y_green)
                print('Distance is:', distance2)
                print('---')
                time.sleep(1)
                if distance2 > 60:
                    cv2.putText(
                        frame,
                        "red: " + str(distance2),
                        (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 0, 255),
                    )
                    # todo figure out when to press and when to release
                    # todo flip x and y, since we have vertical image not horizontal
                    # todo get rid of x_red1
                    if y_green > y_red2:  # move up
                        cv2.putText(
                            frame,
                            "red: " + str(distance2),
                            (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0, 0, 255),
                        )
                        # print("Press!!!")
                        # PressKey(C)
                        # mouse.press(Button.left)
                    elif y_green < y_red2 and distance2 > 60:  # move down
                        cv2.putText(
                            frame,
                            "red: " + str(distance2),
                            (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0, 0, 255),
                        )
                        # print("Release!!!")
                        # ReleaseKey(C)
                    # mouse.release(Button.left)
                else:
                    cv2.putText(
                        frame,
                        "green: " + str(distance2),
                        (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                    )
                    if y_green < y_red2:
                        None
                        # print("Release")
                        # ReleaseKey(C)
                        # mouse.release(Button.left)
                    elif y_green > y_red2:
                        None
                        # print("Press")
                        # PressKey(C)
                        # mouse.press(Button.left)

            except NameError:
                pass

    countours2 = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    y_green_flag = 0
    for contour in countours2:
        area3 = cv2.contourArea(contour)
        if area3 > 5000:  # 5000
            x2, y2, w2, h2 = cv2.boundingRect(contour)
            frame_green = cv2.rectangle(
                frame, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 2
            )

            x_green = int(x2 + w2 / 2)
            y_green = int(y2 + h2 / 2)  # y2 and h2 are both heights of an object
            # Since I know that I can check if fish is between the rectangle heights. I just need center of fish

            cv2.circle(frame, (x_green, y_green), 3, (0, 255, 0), -1)
            cv2.putText(
                frame,
                "green bar",
                (x2 + w2, y2 + h2),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
            )
            cv2.putText(
                frame,
                str(len(countours2)),
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
            )

            try:
                cv2.line(frame, (x_red2, y_red2), (x_green, y_green), (0, 255, 0), 2)

            except NameError:
                pass
    # np.intersect1d(frame_red, frame_green).size
    try:
        if np.array_equal(frame_red, frame_green):  # I have to change the logic here
            cv2.putText(
                frame, f"hooked", (320, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0)
            )
        else:
            cv2.putText(
                frame,
                f"not hooked",
                (320, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 0, 255),
            )
    except NameError:
        cv2.putText(
            frame, "not hooked", (320, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255)
        )
    cv2.imshow("main", frame)
    cv2.waitKey(0)

"""
This is what I understand rn:
1- They made two differant bars, first is red and the other is green
    Even though they are the same bars but the color is differant
    
It takes about 1 second or more for a the rectangle to move from one end to the other

10/10:
    Ideas to make it slow, First one is to make a table 
"""
