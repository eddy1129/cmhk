import cv2
import numpy as np
import matplotlib.pyplot as plt
import urllib.request

# Download the image
image_url = "https://raw.githubusercontent.com/eddy1129/cmhk/master/test1.jpg"
urllib.request.urlretrieve(image_url, "test1.jpg")

# Load the image
image = cv2.imread('test1.jpg')

# Convert the image to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define the color range for detecting the blue line
lower_blue = np.array([100, 50, 50])
upper_blue = np.array([140, 255, 255])

# Create a mask with the blue color range
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Find the coordinates of the blue pixels in the last 500 pixels of the image
blue_coords = np.column_stack(np.where(mask[:, -500:]))

if blue_coords.size > 0:
    # Find the minimum and maximum y-coordinates of the blue pixels
    y_coords = blue_coords[:, 1]
    y_min = np.min(y_coords)
    y_max = np.max(y_coords)

    # Find the x-coordinate where the blue line starts to drop
    x_coords = blue_coords[:, 0]
    x_drop_start = np.min(x_coords[y_coords == y_max])

    # Draw a rectangle to highlight the drop region
    cv2.rectangle(image, (image.shape[1] - 500, x_drop_start), (image.shape[1], y_max), (0, 0, 0), 2)
else:
    print("No blue pixels detected")

# Display the original image with the highlighted area
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title('Highlight Area of Blue Line Drop')
plt.axis('off')
plt.show()
