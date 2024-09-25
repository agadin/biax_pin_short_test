import mss
import cv2
import pytesseract
import numpy as np
import re

def capture_and_decode(monitor):
    with mss.mss() as sct:
        # Capture the specified region of the screen
        img = np.array(sct.grab(monitor))

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Use pytesseract to extract text
        text = pytesseract.image_to_string(gray, config='--psm 6')

        # Extract only numbers from the text
        number = re.findall(r'\d+', text)
        number = ''.join(number) if number else '0'

        return number.strip(), img

if __name__ == "__main__":
    # Example usage with a predefined monitor region
    monitor = {"top": 100, "left": 100, "width": 300, "height": 200}
    decoded_number, captured_image = capture_and_decode(monitor)
    print(f'Decoded Number: {decoded_number}')
    cv2.imshow('Captured Region', captured_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()