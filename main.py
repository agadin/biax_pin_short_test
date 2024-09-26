# Python script that connect to an ardino board and controls a 2 relay module connected to pin 8 on the board
# The script uses the pyserial library to communicate with the ardino board
# have the python script monitor a section the screen and decode a number displayed on the screen
# make the relay controlable via a streamlit web page and display current tension on the streamlit page
import time
import streamlit as st
from screen_decode import capture_and_decode
import pandas as pd
from datetime import datetime
import numpy as np
import cv2
import mss
import serial
import pyautogui

# Initialize serial connection to Arduino
def write_read(x):
    arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

# Function to record event to CSV
def record_event(test_name, tension):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df = pd.DataFrame([[timestamp, tension, test_name]], columns=['Time', 'Tension', 'Test Name'])
    df.to_csv('event_history.csv', mode='a', header=False, index=False)

# Streamlit web page
st.title('Relay Control and Tension Display')

# Input for test name
default_test_name = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
test_name = st.text_input('Test Name', value=default_test_name)

# Toggle for Fire at Threshold
fire_at_threshold = st.checkbox('Fire at Threshold')

# Input for threshold value
threshold_value = st.number_input('Threshold Value', value=0)

# Input for capture zone
with st.expander("Capture Zone Settings"):
    capture_top = st.number_input('Capture Top', value=390)
    capture_left = st.number_input('Capture Left', value=590)
    capture_width = st.number_input('Capture Width', value=150)
    capture_height = st.number_input('Capture Height', value=25)

# Add input fields for user-supplied coordinates
with st.expander("Button Coordinates"):
    button_top = st.number_input('Button Top', value=100)
    button_left = st.number_input('Button Left', value=100)
    button_width = st.number_input('Button Width', value=50)
    button_height = st.number_input('Button Height', value=30)

# Dropdown for selecting outcome
outcome = st.selectbox('Select Outcome', ['Fire Relay', 'Click Next Button'])

# Relay control
if outcome == 'Fire Relay':
    fire_message = st.empty()
    delay_input = st.number_input('Relay Delay', value=0.5)
    if st.button('Turn Relay On'):
        write_read('ON')
        # fire_message.write('Relay is turned on')
        tension, img = capture_and_decode({"top": capture_top, "left": capture_left, "width": capture_width, "height": capture_height})
        record_event(test_name, tension)
        time.sleep(delay_input)  # Wait for half a second
        write_read('OFF')
        # fire_message.write('Relay is turned off')
        tension, img = capture_and_decode({"top": capture_top, "left": capture_left, "width": capture_width, "height": capture_height})
        record_event(test_name, tension)

# Placeholder for current tension, image, and line chart
tension_placeholder = st.empty()
chart_placeholder = st.empty()
image_placeholder = st.empty()
next_button_place = st.empty()

# List to store tension values for plotting
tension_values = []

if st.button('Show Event History'):
    try:
        history_df = pd.read_csv('event_history.csv', names=['Time', 'Tension', 'Test Name'])
        st.write(history_df)
    except FileNotFoundError:
        st.write('No event history found.')


# Continuously update tension
while True:
    tension, img = capture_and_decode({"top": capture_top, "left": capture_left, "width": capture_width, "height": capture_height})
    tension_placeholder.text(f'Current Tension: {tension}')
    image_placeholder.image(img, caption='Captured Region', use_column_width=True)

    # Append current tension to the list
    tension_values.append(float(tension))

    # Display the tension values as a line chart
    chart_placeholder.line_chart(tension_values)
    if outcome == 'Click Next Button':
        tension_hold, cropped_img = capture_and_decode({"top": button_top, "left": button_left, "width": button_width, "height": button_height})
    # Ensure cropping coordinates are within the image bound
        next_button_place.image(cropped_img, caption='Current Location of Next Button', use_column_width=True)


    # Check if tension exceeds threshold and fire at threshold is enabled
    if fire_at_threshold and float(tension) > threshold_value:
        if outcome == 'Fire Relay':
            write_read('ON')
            st.write('Relay is turned on due to threshold')
            record_event(test_name, tension)
        elif outcome == 'Click Next Button':
            pyautogui.click(button_left + button_width // 2, button_top + button_height // 2)
            st.write('Next button clicked due to threshold')
            record_event(test_name, tension)

    time.sleep(1)  # Update every second