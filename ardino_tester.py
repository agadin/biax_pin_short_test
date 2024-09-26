import streamlit as st
import serial
import time

# Function to send command to Arduino and read response
def write_read(command):
    try:
        arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)
        time.sleep(2)  # Wait for the connection to establish
        arduino.write(bytes(command, 'utf-8'))
        time.sleep(0.1)
        data = arduino.readline().decode('utf-8').strip()
        arduino.close()
        return data
    except serial.SerialException as e:
        return f"Error: {e}"

# Streamlit web page
st.title('Arduino Command Sender')

# Button to send command to Arduino
if st.button('Send Command'):
    response = write_read('YOUR_COMMAND_HERE')
    st.write(f'Arduino response: {response}')