import pyautogui
import time

# Coordinates of the window to click
window_x = 100  # Replace with your window's X coordinate
window_y = 200  # Replace with your window's Y coordinate

# Number of clicks
click_count = 10

# Delay between clicks in seconds
delay = 1

for _ in range(click_count):
    pyautogui.click(window_x, window_y)
    time.sleep(delay)