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

# Define color thresholds for blue and orange
lower_blue = np.array([100, 0, 0], dtype=np.uint8)
upper_blue = np.array([255, 100, 100], dtype=np.uint8)

lower_orange = np.array([0, 50, 150], dtype=np.uint8)
upper_orange = np.array([100, 150, 255], dtype=np.uint8)

# Create masks to identify blue and orange pixels
blue_pixels = cv2.inRange(roi, lower_blue, upper_blue)
orange_pixels = cv2.inRange(roi, lower_orange, upper_orange)

# Find the coordinates of blue and orange pixels
blue_coords = np.column_stack(np.where(blue_pixels))
orange_coords = np.column_stack(np.where(orange_pixels))

# Find the region where blue is below orange
below_region = []
for bx, by in blue_coords:
    for ox, oy in orange_coords:
        if bx > ox and by == oy:
            below_region.append((bx, by))

# If we found a region where blue is below orange
if below_region:
    below_region = np.array(below_region)
    x_min, x_max = np.min(below_region[:, 0]), np.max(below_region[:, 0])
    y_min, y_max = np.min(below_region[:, 1]), np.max(below_region[:, 1])

    # Draw a rectangle on the original image to highlight the area
    cv2.rectangle(image, (roi_x + y_min, x_min), (roi_x + y_max, x_max), (0, 0, 255), 2)

# Display the original image with the highlighted area
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title('Highlight Area When Blue Line is Below Orange Line')
plt.axis('off')
plt.show()
