import time
import streamlit as st
from screen_decode import capture_and_decode
import pandas as pd
from datetime import datetime
import numpy as np
import cv2
import mss

# Mock Arduino class for testing without actual hardware
class MockArduino:
    def __init__(self):
        self.state = 'OFF'

    def write(self, command):
        if command == b'ON':
            self.state = 'ON'
        elif command == b'OFF':
            self.state = 'OFF'

    def readline(self):
        return f'Relay is turned {self.state}\n'.encode()

# Use MockArduino instead of serial.Serial for testing
arduino = MockArduino()

def write_read(x):
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
    top = st.number_input('Top', value=100)
    left = st.number_input('Left', value=100)
    width = st.number_input('Width', value=300)
    height = st.number_input('Height', value=200)

# Relay control
if st.button('Turn Relay On'):
    write_read('ON')
    st.write('Relay is turned on')
    tension, img = capture_and_decode({"top": top, "left": left, "width": width, "height": height})
    record_event(test_name, tension)
    time.sleep(0.5)  # Wait for half a second
    write_read('OFF')
    st.write('Relay is turned off')
    tension, img = capture_and_decode({"top": top, "left": left, "width": width, "height": height})
    record_event(test_name, tension)

# Placeholder for current tension, image, and line chart
tension_placeholder = st.empty()
chart_placeholder = st.empty()
image_placeholder = st.empty()


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
    tension, img = capture_and_decode({"top": top, "left": left, "width": width, "height": height})
    tension_placeholder.text(f'Current Tension: {tension}')
    # Display the tension values as a line chart
    chart_placeholder.line_chart(tension_values)

    image_placeholder.image(img, caption='Captured Region', use_column_width=True)

    # Append current tension to the list
    tension_values.append(float(tension))



    # Check if tension exceeds threshold and fire at threshold is enabled
    if fire_at_threshold and float(tension) > threshold_value:
        write_read('ON')
        st.write('Relay is turned on due to threshold')
        record_event(test_name, tension)

    time.sleep(1)  # Update every second