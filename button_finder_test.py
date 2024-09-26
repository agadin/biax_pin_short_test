import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load the trained model
model = load_model('button_finder_model.h5')

# Function to preprocess the image
def preprocess_image(img_path, img_size=(224, 224)):
    img = cv2.imread(img_path)
    img_resized = cv2.resize(img, img_size)
    img_normalized = img_resized / 255.0
    return img, np.expand_dims(img_normalized, axis=0)

# Select an image from the images folder
image_folder = 'images'
image_file = 'screen1.png'  # Change this to any image file from the folder
img_path = os.path.join(image_folder, image_file)

# Preprocess the image
original_img, preprocessed_img = preprocess_image(img_path)

# Predict the bounding box coordinates
predicted_coords = model.predict(preprocessed_img)[0]

# Denormalize the coordinates
img_height, img_width, _ = original_img.shape
x1, y1, x2, y2 = predicted_coords * [img_width, img_height, img_width, img_height]
x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

# Print the coordinates
print(f'Predicted coordinates: x1={x1}, y1={y1}, x2={x2}, y2={y2}')

# Ensure coordinates are within image bounds
x1 = max(0, min(x1, img_width))
y1 = max(0, min(y1, img_height))
x2 = max(0, min(x2, img_width))
y2 = max(0, min(y2, img_height))

# Crop the image around the bounding box
cropped_img = original_img[y1:y2, x1:x2]

# Check if the cropped image is empty
if cropped_img.size == 0:
    print("Error: Cropped image is empty. Check the coordinates.")
else:
    # Save the cropped image as a new file
    cropped_img_path = os.path.join(image_folder, 'cropped_' + image_file)
    cv2.imwrite(cropped_img_path, cropped_img)
    print(f'Cropped image saved as {cropped_img_path}')

# Draw the predicted bounding box on the original image
cv2.rectangle(original_img, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Display the original image with the predicted bounding box
cv2.imshow('Predicted Button', original_img)
cv2.waitKey(0)
cv2.destroyAllWindows()