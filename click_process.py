# click_process.py
import pyautogui
import time
import sys

def perform_click(button_top, button_left, button_width, button_height):
    click_count = 0
    while click_count < 10:
        pyautogui.click(button_left + button_width // 2, button_top + button_height // 2)
        time.sleep(1)
        click_count += 1

if __name__ == "__main__":
    button_top = int(sys.argv[1])
    button_left = int(sys.argv[2])
    button_width = int(sys.argv[3])
    button_height = int(sys.argv[4])
    perform_click(button_top, button_left, button_width, button_height)