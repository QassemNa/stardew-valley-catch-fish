import time
from cv2 import cv2
import numpy as np

from Stardew.utils.screen import grab_screen, main_screen


def extract_reel_data(frame=cv2.imread("Screenshots/Screenshot_3.png"), sleep=0.1):
    # init
    fish_x_coordinate = False
    fish_y_coordinate = False
    bar_x_coordinate = False
    bar_y_coordinate = False
    frame_red = False
    frame_green = False

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
    contours_blue = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

    for contour in contours_blue:
        area2 = cv2.contourArea(contour)

        if 950 > area2 > 200:
            fish_border_x_coordinate, fish_border_Y_coordinate, fish_width, fish_height = cv2.boundingRect(contour)
            frame_red = cv2.rectangle(
                frame, (fish_border_x_coordinate, fish_border_Y_coordinate), (fish_border_x_coordinate + fish_width,
                                                                              fish_border_Y_coordinate + fish_height),
                (0, 34, 255), 2
            )
            fish_x_coordinate = int(fish_border_x_coordinate + fish_width / 2)  # x coordinate of fish
            fish_y_coordinate = int(fish_border_Y_coordinate + fish_height / 2)  # y coordinate of fish
            cv2.circle(frame, (fish_x_coordinate, fish_y_coordinate), 3, (0, 34, 255), -1)
            cv2.putText(
                frame,
                "Fish",
                (fish_border_x_coordinate + fish_width, fish_border_Y_coordinate + fish_height),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 34, 255),
            )

    contours_green = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    for contour in contours_green:

        area3 = cv2.contourArea(contour)
        # size of the bar fluctuates between 5000 and 6607. 7200 is when reel progress turns green
        if 5000 < area3 < 7200:
            bar_border_x_coordinate, bar_border_y_coordinate, bar_width, bar_height = cv2.boundingRect(contour)
            frame_green = cv2.rectangle(
                frame, (bar_border_x_coordinate, bar_border_y_coordinate),
                (bar_border_x_coordinate + bar_width, bar_border_y_coordinate + bar_height), (0, 255, 0), 2
            )

            bar_x_coordinate = int(bar_border_x_coordinate + bar_width / 2)
            bar_y_coordinate = int(bar_border_y_coordinate + bar_height / 2)
            # Since I know that I can check if fish is between the rectangle heights. I just need center of fish

            cv2.circle(frame, (bar_x_coordinate, bar_y_coordinate), 3, (0, 255, 0), -1)
            cv2.putText(
                frame,
                "bar",
                (bar_border_x_coordinate + bar_width, bar_border_y_coordinate + bar_height),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
            )
            cv2.putText(
                frame,
                str(len(contours_green)),
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
            )

    is_fish_exist = fish_x_coordinate and fish_y_coordinate and frame_red.any()
    is_bar_exist = bar_x_coordinate and bar_y_coordinate and frame_green.any()

    if is_fish_exist and is_bar_exist:
        cv2.line(frame, (fish_x_coordinate, fish_y_coordinate), (bar_x_coordinate, bar_y_coordinate),
                 (0, 255, 0), 2)

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
    # np.intersect1d(frame_red, frame_green).size

    cv2.imshow("main", frame)
    cv2.waitKey(int(sleep * 1000))

    # all the things before are just to make things visible
    # now the real magic starts


"""
This is what I understand rn:
1- They made two different bars, first is red and the other is green
    Even though they are the same bars but the color is different
    
It takes about 1 second or more for a the rectangle to move from one end to the other

10/10:
    Ideas to make it slow, First one is to make a table 
"""
