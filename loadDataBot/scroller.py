import pyautogui
from time import sleep

screenHeight = pyautogui.size().height

try:
    while True:
        pyautogui.moveTo(200, int(screenHeight / 2))
        pyautogui.drag(1100, 0, duration=0.11, button='left')
        sleep(1)
except KeyboardInterrupt:
    print("Bot stopped by user.")