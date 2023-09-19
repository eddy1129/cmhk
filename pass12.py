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
        significant_changes.append((x, y, w, h))

# Find the rightmost rectangle among the significant changes
if significant_changes:
    rightmost_rectangle = max(significant_changes, key=lambda rect: rect[0] + rect[2])
    x, y, w, h = rightmost_rectangle
    
    # Draw the rightmost rectangle on the original image
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

# Display the original image with the rightmost significant change highlighted using a rectangle
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title('Rightmost Significant Change (Highlighted with a Rectangle)')
plt.axis('off')
plt.show()
