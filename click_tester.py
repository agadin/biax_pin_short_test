import streamlit as st
import pyautogui
import time
import threading

# Event to control the clicking process
click_event = threading.Event()

# Function to perform the click action
def perform_click(button_top, button_left, button_width, button_height):
    click_count = 0
    while click_event.is_set() and click_count < 10:
        pyautogui.click(button_left + button_width // 2, button_top + button_height // 2)
        time.sleep(1)
        click_count += 1
        if not click_event.is_set():
            break

# Function to start the click thread
def start_click_thread(button_top, button_left, button_width, button_height):
    click_event.set()
    threading.Thread(target=perform_click, args=(button_top, button_left, button_width, button_height)).start()

# Streamlit web page
st.title('Automated Screen Clicker')

# Dropdown for selecting outcome
outcome = st.selectbox('Select Outcome', ['Click Next Button'])

# Add input fields for user-supplied coordinates
with st.expander("Button Coordinates"):
    button_top = st.number_input('Button Top', value=347)
    button_left = st.number_input('Button Left', value=1538)
    button_width = st.number_input('Button Width', value=50)
    button_height = st.number_input('Button Height', value=50)

# Button to start the test
if st.button('Start Test'):
    start_click_thread(button_top, button_left, button_width, button_height)

# Button to stop the test
if st.button('Stop Test'):
    click_event.clear()