from Stardew.utils.extract_reel_data import extract_reel_data
from Stardew.utils.screen import main_screen
import mss
import time

SCT = mss.mss()
SLEEP = 0.1
while 1:
    extract_reel_data(frame=main_screen(screen_shot=SCT, just_reel=True), sleep=SLEEP)
    time.sleep(SLEEP)
