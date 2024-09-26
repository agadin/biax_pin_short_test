import streamlit as st
import subprocess

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

# Initialize session state for the click process
if 'click_process' not in st.session_state:
    st.session_state['click_process'] = None

# Button to start the test
if st.button('Start Test'):
    if st.session_state['click_process'] is None or st.session_state['click_process'].poll() is not None:
        st.session_state['click_process'] = subprocess.Popen([
            'python', 'click_process.py', str(button_top), str(button_left), str(button_width), str(button_height)
        ])

# Button to stop the test
if st.button('Stop Test'):
    if st.session_state['click_process'] is not None:
        st.session_state['click_process'].terminate()
        st.session_state['click_process'] = None