# Overview
A streamlit application to automatically decode numbers from a windowed gui (ie machine output readout) and trigger an Arduino relay connected to the host computer.
* [Introduction](#introduction)
* [Installation](#installation)
* [Usage](#usage)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)

# Introduction
`streamlit-arduino-relay` is a streamlit application to automatically decode numbers from a windowed gui (ie machine output readout) and trigger an Arduino relay or a screen click when a specific threshold value has been reached.

## Decoding GUI Numbers
The main application (`main.py`) first reads a select region of the screen. The user defines this region (labeled `Captured Region` in the streamlit application) by indicating the top left corner cordinates and the height and width of the box they would like to capture. A preview of this region can be seen in the streamlit web application. From the region, a using `pytesseract` the text is extracted from the image. The extracted text is then converted to a number and compared to a threshold value. The regex pattern used to parse only the numbers will remove all non-number characters while keeping the deimal point. The extracted number is shown on the web applicaiton as `Current Tension:` and is a float value. A temporal history of the read value is shown in the chart in the application.

## Outcomes
The code currently has two outcomes when the threshold value is reached:
* Trigger an Arduino relay connected to the host computer
* Trigger a screen click at the location of the captured region

These outcomes can be toggled on and off in the streamlit application by using the dropdown labeled `Select Outcome`. The relay is triggered using the `pyserial` library and the screen click is triggered using the `pyautogui` library. 

In the arduino relay outcome, an Arduino connected to `COM3` of the computer (this can be changed in the `main.py` file) is triggered when the threshold value is reached. The relay is connected to the Arduino and the Arduino is connected to the computer via USB. The relay is triggered for a variable time (Default 1 second) when the threshold value is reached. The relay is triggered using the `pyserial` library. To set up the arduino see the [Installation](#installation) section.

In the screen click outcome, a screen click is triggered at the location of the captured region when the threshold value is reached. The screen click is triggered using the `pyautogui` library. The screen click is triggered for (Default 1 second) when the threshold value is reached.

For each time an outcome is activated by a threshold value, the time and value are logged in a csv file. The csv file is saved in the `data` directory and is named `tension_log.csv`. The csv file has the following columns:
* `timestamp`: The time the threshold value was reached
* `tension`: The value of the threshold reached

# Installation
1. clone the repository
```bash
git clone [Repository URL]
```

2.  Install the required packages, run the following command in the root directory of the project:
```bash
pip install -r requirements.txt
```
3. Set up the Arduino
* Install [Arduino IDE](https://www.arduino.cc/en/software) (if not already installed)
* Connect the relay to the Arduino by conntecing the `IN1` of the relay to the digital pin 8 of the Arduino, the GND of the relay to the GND of the Arduino, and the VCC of the relay to the 5V of the Arduino. 
* Connect the Arduino to the computer via USB
* Load `biax_short.ino` onto the Arduino using the Arduino IDE by navigating to the cloned repository folder and opening the `biax_short.ino` file in the Arduino IDE. Then upload the code to the Arduino.
* Note the COM port of the Arduino (this can be found in the Arduino IDE under `Tools > Port`). If it is not `COM3` change the `COM_PORT` variable in the `main.py` file to the correct port.

## Shorting the biax pin
The arduino relay is used to short the ground pin (Pin 8) and pin 13 of the M port on the biax. To do this connect a jumper cable from `COM1` of the relay to the ground pin (Pin 8) of the biax and connect a jumper cable from `NC1` of the arduino to pin 13 of the M port of the biax. This will serve as a digital input for the biax and can be used to stop the current section, stop completely depending on how it is set up in the Newton software. 

> [!IMPORTANT]
> The digital input is set to active HIGH (pull-up resistor set to active), meaning that the biax will stop when the pin is shorted to ground.

# Usage
To run the streamlit application, run the following command in the root directory of the project (where the `main.py` file is located, can be run in the terminal or command prompt and navigated to by using the `cd` command):
```bash
streamlit run main.py
```
A webrowser window should open with the streamlit application. The application has the following sections:
* `Captured Region`: This section allows the user to define the region of the screen they would like to capture. The user can define the top left corner of the region by inputting the x and y coordinates in the `Top Left Corner` section. The user can define the height and width of the region by inputting the height and width in the `Height` and `Width` sections. The user can preview the region by clicking the `Preview Captured Region` button. The user can capture the region by clicking the `Capture Region` button. The captured region will be shown in the streamlit application.
* `Current Tension`: This section shows the current tension value read from the captured region. The value is a float value and is updated every time the `Update Tension` button is clicked.
* `Select Outcome`: This section allows the user to select the outcome when the threshold value is reached. The user can select `Arduino Relay` to trigger the Arduino relay when the threshold value is reached or `Screen Click` to trigger a screen click at the location of the captured region when the threshold value is reached.
* `Threshold Value`: This section allows the user to set the threshold value. The user can input the threshold value in the `Threshold Value` section. The user can update the threshold value by clicking the `Update Threshold` button.
* `Trigger Outcome`: This section allows the user to trigger the outcome manually. The user can trigger the outcome by clicking the `Trigger Outcome` button.
* `Tension History`: This section shows the history of the tension values read from the captured region. The history is shown in a chart and is updated every time the `Update Tension` button is clicked.
* `Log`: This section shows the log of the threshold values reached and the time they were reached. The log is saved in a csv file in the `data` directory and is named `tension_log.csv`.

Depending on the state of `Select Outcome` different windows will appear:
* If `Arduino Relay` is selected, the user will need to have the Arduino connected to the computer and the relay connected to the Arduino. If this outcome is selected the user can manually trigger the relay by clicking the `Trigger Relay` button. By default, automatic triggering of the relay when the threshold is surpassed will occur which can be turned off by toggling the `Fire at Threshold` toggle to off. The duration between the relay turning on and off can be changed by changing the `Relay Delay` variable in the input field in the streamlit application.
* If `Screen Click` is selected, a second capture window appears below showing the location of the button on the screen specified by the user. The user can manually edit the location and size of the button by changing the `Button Location` and `Button Size` input fields. The user can manually trigger the screen click by clicking the `Trigger Screen Click` button. By default, automatic triggering of the screen click when the threshold is surpassed will occur which can be turned off by toggling the `Fire at Threshold` toggle to off. 

## Running the Application
1. Plug in the ardunio to the computer and connect the relay to the arduino as described in the [Installation](#installation) section.
2. In anaconda, naviagte to enviroments on the left and click on the enviroment called base(root). Then click on the play button and select 'Open in Terminal' from the drop down. 
3. In the terminal, navigate to the directory where the `main.py` file is located using the `cd` command followed by the file path.
4. Run the streamlit application by running the following command in the terminal:
```bash
streamlit run main.py
```
5. A web browser window should open with the streamlit application. The user can interact with the application as described in the [Usage](#usage) section.
6. Change the name of the test in the webrowser (optional)
7. Change the location of the capture window to the desired location on the screen where the numbers are displayed by `Top Left Corner` and `Height` and `Width` in the `Captured Region` drop down.
8. Change the threshold value to the desired value in the `Threshold Value` drop down and toggle the `Fire at Threshold` toggle to on.
9. select the outcome you would like to trigger when the threshold value is reached in the `Select Outcome` drop down.
10. Begin the test on the biax software and the application will automatically trigger the outcome when the threshold value is reached.
11. The code will continue to trigger the relay every 10 seconds the observed value reminds above the threshold value. This can be changed by editing `main.py` and changing the `time.sleep(10)` to the desired time in seconds.

> [!IMPORTANT]
> The code will continue to trigger the relay every 10 seconds the observed value reminds above the threshold value

> [!NOTE]
> `crtl + c` can be used to stop the streamlit application in the terminal
# Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.
* @agadin on github

# License
Distributed under the MIT License. See `LICENSE` for more information.

# Contact
* @agadin on github

# Acknowledgements
* [Streamlit](https://streamlit.io/)
* [Pytesseract](https://pypi.org/project/pytesseract/)
* [Pyserial](https://pypi.org/project/pyserial/)
* [Pyautogui](https://pypi.org/project/PyAutoGUI/)
* [Arduino](https://www.arduino.cc/en/software)
* [Newton](https://www.newtonresearch.co.uk/)
* [Biax](https://www.newtonresearch.co.uk/)