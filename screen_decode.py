import mss
import cv2
import pytesseract
import numpy as np
import re
import pyautogui

def capture_and_decode(monitor):
    with mss.mss() as sct:
        print(f"Capturing screen region: {monitor}")
        img = np.array(sct.grab(monitor))
        print("Screen region captured.")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print("Converted image to grayscale.")

        text = pytesseract.image_to_string(gray, config='--psm 6')
        print(f"Extracted text: {text}")

        number = re.findall(r'\d+', text)
        number = ''.join(number) if number else '0'
        print(f"Extracted number: {number}")

        return number.strip(), img

import mss
import cv2

def highlight_next_button():
    with mss.mss() as sct:
        print("Capturing full screen.")
        img = np.array(sct.grab(sct.monitors[1]))
        print("Full screen captured.")

        template = cv2.imread('next_button_2.png', cv2.IMREAD_GRAYSCALE)
        if template is None:
            print("Error: Template image not found.")
            return img
        print("Template image loaded.")

        template_w, template_h = template.shape[::-1]
        print(f"Template size: width={template_w}, height={template_h}")

        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print("Converted full screen image to grayscale.")

        result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print(f"Template matching results: min_val={min_val}, max_val={max_val}, min_loc={min_loc}, max_loc={max_loc}")

        # Check if the match is above a certain threshold
        threshold = 0.5
        if max_val < threshold:
            print(f"No match found above threshold. Max value: {max_val}")
            return img

        top_left = max_loc
        bottom_right = (top_left[0] + template_w, top_left[1] + template_h)
        cv2.rectangle(img, top_left, bottom_right, (255, 0, 0), 2)
        print(f"Drew rectangle: top_left={top_left}, bottom_right={bottom_right}")

        # Save the image to a file for verification
        cv2.imwrite('highlighted_image.png', img)
        print("Saved highlighted image to 'highlighted_image.png'")

        return img

if __name__ == "__main__":
    highlighted_image = highlight_next_button()
    cv2.imshow('Highlighted Next Button', highlighted_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
