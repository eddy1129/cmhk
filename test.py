import cv2
import numpy as np
import matplotlib.pyplot as plt
import urllib.request

# Download the image
# image_url = "https://raw.githubusercontent.com/eddy1129/cmhk/master/test3.jpg"
# urllib.request.urlretrieve(image_url, "test3.jpg")

# Load the image
image = cv2.imread('test2.jpg')

# Convert the image to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define the color range for detecting the blue and orange lines
lower_blue = np.array([100, 50, 50])
upper_blue = np.array([140, 255, 255])

lower_orange = np.array([5, 50, 50])
upper_orange = np.array([20, 255, 255])

# Create masks to identify blue and orange pixels in the entire image
mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)

# Find the coordinates of the blue and orange pixels
blue_coords = np.column_stack(np.where(mask_blue))
orange_coords = np.column_stack(np.where(mask_orange))

# Function to find and highlight the area where the blue line drops and does not touch the orange line
def find_and_highlight_drop_area(blue_coords, orange_coords):
    if blue_coords.size > 0 and orange_coords.size > 0:
        drop_start_x = None
        drop_start_y = None
        drop_lowest_x = None
        drop_highest_x = None

        for x in range(image.shape[1]):
            blue_y_at_x = blue_coords[blue_coords[:, 1] == x][:, 0]
            orange_y_at_x = orange_coords[orange_coords[:, 1] == x][:, 0]

            if blue_y_at_x.size > 0 and orange_y_at_x.size > 0:
                blue_y_max_at_x = np.max(blue_y_at_x)
                blue_y_min_at_x = np.min(blue_y_at_x)
                orange_y_min_at_x = np.min(orange_y_at_x)

                if drop_start_x is None and blue_y_max_at_x > orange_y_min_at_x:
                    drop_start_x = blue_y_min_at_x
                    drop_start_y = x
                    drop_lowest_x = blue_y_max_at_x
                    drop_highest_x = blue_y_min_at_x
                elif drop_start_x is not None:
                    drop_lowest_x = max(drop_lowest_x, blue_y_max_at_x)
                    drop_highest_x = min(drop_highest_x, blue_y_min_at_x)
                    if blue_y_max_at_x <= orange_y_min_at_x:
                        y_max = x

                        # Draw a rectangle to highlight the drop area
                        cv2.rectangle(image, (drop_start_y, drop_highest_x), (y_max, drop_lowest_x), (0, 0, 255), 2)
                        drop_start_x = None
                        drop_start_y = None
                        drop_lowest_x = None
                        drop_highest_x = None

        # If the blue line does not touch the orange line at the end of the image, highlight the last drop area
        if drop_start_x is not None:
            x_max = np.max(blue_coords[blue_coords[:, 1] >= drop_start_y][:, 0])
            y_max = image.shape[1]

            # Draw a rectangle to highlight the last drop area
            cv2.rectangle(image, (drop_start_y, drop_highest_x), (y_max, x_max), (0, 0, 255), 2)





# Find and highlight the drop areas
find_and_highlight_drop_area(blue_coords, orange_coords)

# Display the original image with the highlighted areas
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title('Highlight Drop Areas')
plt.axis('off')
plt.show()
