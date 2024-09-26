import streamlit as st
import pyautogui
import time
import threading

if 'clicking' not in st.session_state:
    st.session_state['clicking'] = False

# Function to perform the click action
def perform_click(button_top, button_left, button_width, button_height):
    while st.session_state['clicking']:
        pyautogui.click(button_left + button_width // 2, button_top + button_height // 2)
        time.sleep(1)

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

# Initialize session state for clicking
if 'clicking' not in st.session_state:
    st.session_state['clicking'] = False

# Button to start the test
if st.button('Start Test'):
    st.session_state['clicking'] = True
    threading.Thread(target=perform_click, args=(button_top, button_left, button_width, button_height)).start()

# Button to stop the test
if st.button('Stop Test'):
    st.session_state['clicking'] = False