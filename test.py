import cv2
import numpy as np
import matplotlib.pyplot as plt
import urllib.request

# Download the image
image_url = "https://raw.githubusercontent.com/eddy1129/cmhk/master/test3.jpg"
urllib.request.urlretrieve(image_url, "test3.jpg")

# Load the image
image = cv2.imread('test3.jpg')

# Define the region of interest (ROI) for the right side of the image
roi_x = image.shape[1] - 500  # Start from the last 500 pixels of the image
roi_width = 500  # Width of the ROI

# Crop the ROI from the image
roi = image[:, roi_x:roi_x + roi_width]

# Define color thresholds for blue
lower_blue = np.array([100, 0, 0], dtype=np.uint8)
upper_blue = np.array([255, 100, 100], dtype=np.uint8)

# Create masks to identify blue pixels
blue_pixels = cv2.inRange(roi, lower_blue, upper_blue)

# Find the coordinates of blue pixels
blue_coords = np.column_stack(np.where(blue_pixels))

# Find the region where there is a significant drop in the blue line
drop_region = []
prev_y = None
for bx, by in blue_coords:
    if prev_y is not None and bx > prev_y + 5:  # Adjust the threshold as needed
        drop_region.append((bx, by))
    prev_y = bx

# If we found a region where there is a significant drop in the blue line
if drop_region:
    drop_region = np.array(drop_region)
    x_min, x_max = np.min(drop_region[:, 0]), np.max(drop_region[:, 0])
    y_min, y_max = np.min(drop_region[:, 1]), np.max(drop_region[:, 1])

    # Draw a rectangle on the original image to highlight the area
    cv2.rectangle(image, (roi_x + y_min, x_min), (roi_x + y_max, x_max), (0, 0, 0), 2)

# Display the original image with the highlighted area
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title('Highlight Area of Blue Line Drop')
plt.axis('off')
plt.show()
