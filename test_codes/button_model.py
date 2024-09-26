import os
import pandas as pd
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.applications import VGG16
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam

# Load dataset
data_dir = 'images'
labels_file = 'labels.csv'
labels = pd.read_csv(labels_file)

# Preprocess images and labels
def preprocess_data(data_dir, labels, img_size=(224, 224)):
    images = []
    coords = []
    for index, row in labels.iterrows():
        img_path = os.path.join(data_dir, row['filename'])
        img = cv2.imread(img_path)
        img = cv2.resize(img, img_size)
        images.append(img)
        coords.append([row['x1'], row['y1'], row['x2'], row['y2']])
    images = np.array(images) / 255.0  # Normalize pixel values
    coords = np.array(coords) / [img_size[0], img_size[1], img_size[0], img_size[1]]  # Normalize coordinates
    return images, coords

images, coords = preprocess_data(data_dir, labels)
X_train, X_test, y_train, y_test = train_test_split(images, coords, test_size=0.2, random_state=42)

# Data augmentation
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Load VGG16 model + higher level layers
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
x = base_model.output
x = Flatten()(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.5)(x)
predictions = Dense(4)(x)  # Output layer for x1, y1, x2, y2 coordinates

model = Model(inputs=base_model.input, outputs=predictions)

# Freeze the layers of VGG16
for layer in base_model.layers:
    layer.trainable = False

model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_absolute_error', metrics=['accuracy'])

# Train the model with data augmentation
history = model.fit(datagen.flow(X_train, y_train, batch_size=32), epochs=50, validation_data=(X_test, y_test))

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')

# Save the model
model.save('button_finder_model.h5')
print('Model saved as button_finder_model.h5')