import pyautogui
import pygetwindow as gw
import time

# Name of the window to focus
window_title = "Your Window Title"  # Replace with the title of your window

# Coordinates of the window to click
window_x = 100  # Replace with your window's X coordinate
window_y = 200  # Replace with your window's Y coordinate

# Number of clicks
click_count = 10

# Delay between clicks in seconds
delay = 1

# Find and focus the window
window = gw.getWindowsWithTitle(window_title)
if window:
    window[0].activate()
    time.sleep(1)  # Give some time for the window to come to focus

    for _ in range(click_count):
        pyautogui.click(window_x, window_y)
        time.sleep(delay)
else:
    print(f"Window with title '{window_title}' not found.")