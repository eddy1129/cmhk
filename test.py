import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread('test3.jpg')

# Preprocess the image (convert to grayscale and apply Gaussian blur)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply Canny edge detection
edges = cv2.Canny(blurred, threshold1=30, threshold2=100)

# Find contours in the edge-detected image
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter out small contours (noise)
min_contour_area = 100
significant_changes = []

for contour in contours:
    if cv2.contourArea(contour) > min_contour_area:
        x, y, w, h = cv2.boundingRect(contour)
        if x > image.shape[1] // 2:  # Only consider contours on the right side
            significant_changes.append((x, y, w, h))

# Get the largest contour on the right side (assumed to be the blue line)
if significant_changes:
    largest_contour = max(significant_changes, key=lambda rect: rect[2] * rect[3])
    x, y, w, h = largest_contour

    # Draw a rectangle around the largest contour
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

# Display the original image with the significant change of the blue line highlighted
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title('Significant Change in Blue Line (Highlighted with a Rectangle)')
plt.axis('off')
plt.show()
