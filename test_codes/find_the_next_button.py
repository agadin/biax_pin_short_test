import cv2
import os
import pandas as pd

# Initialize global variables
drawing = False
ix, iy = -1, -1
ex, ey = -1, -1
bounding_boxes = []

# Mouse callback function to draw bounding box
def draw_rectangle(event, x, y, flags, param):
    global ix, iy, ex, ey, drawing, bounding_boxes

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            ex, ey = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        ex, ey = x, y
        bounding_boxes.append((ix, iy, ex, ey))

# Function to label images
def label_images(image_folder, output_csv):
    global ix, iy, ex, ey, bounding_boxes

    # Get list of images
    images = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    labeled_data = []

    for image_file in images:
        img_path = os.path.join(image_folder, image_file)
        img = cv2.imread(img_path)
        clone = img.copy()

        cv2.namedWindow('image')
        cv2.setMouseCallback('image', draw_rectangle)

        while True:
            img = clone.copy()
            if drawing:
                cv2.rectangle(img, (ix, iy), (ex, ey), (0, 255, 0), 2)
            cv2.imshow('image', img)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('n'):  # Press 'n' to go to the next image
                if bounding_boxes:
                    for box in bounding_boxes:
                        x1, y1, x2, y2 = box
                        labeled_data.append([image_file, x1, y1, x2, y2])
                bounding_boxes = []
                break
            elif key == ord('q'):  # Press 'q' to quit
                cv2.destroyAllWindows()
                return labeled_data

        cv2.destroyAllWindows()

    return labeled_data

# Main function
if __name__ == "__main__":
    image_folder = 'images'
    output_csv = 'labels.csv'

    labeled_data = label_images(image_folder, output_csv)
    df = pd.DataFrame(labeled_data, columns=['filename', 'x1', 'y1', 'x2', 'y2'])
    df.to_csv(output_csv, index=False)
    print(f"Labels saved to {output_csv}")