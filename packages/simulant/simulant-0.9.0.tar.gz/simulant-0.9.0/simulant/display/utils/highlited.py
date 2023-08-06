import cv2
import numpy as np


def find_highlighted(before_img_path, after_img_path):
    # Load both images
    img_before = cv2.imread(before_img_path)
    img_after = cv2.imread(after_img_path)
    # Convert images to grayscale
    gray_before = cv2.cvtColor(img_before, cv2.COLOR_BGR2GRAY)
    gray_after = cv2.cvtColor(img_after, cv2.COLOR_BGR2GRAY)
    # Calculate difference between the two images
    diff = cv2.absdiff(gray_before, gray_after)
    # Threshold the difference image to highlight the selected area
    thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Check if contours were found
    if len(contours) == 0:
        return None
    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)
    # Draw a bounding box around the largest contour
    x, y, w, h = cv2.boundingRect(largest_contour)
    # Return the coordinates of the bounding box
    return (x, y), (x + w, y + h)


def find_highlight_yellow(image, min_area=100):
    # Load the image
    img = np.array(image)[:, :, ::-1].copy()
    # img = cv2.imread(str(image_path))
    # Convert the image from BGR to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Define the range of yellow color in HSV color space
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    # Threshold the image to get only yellow pixels
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    # Bitwise-AND mask and original image to extract yellow pixels
    res = cv2.bitwise_and(img, img, mask=mask)
    # Convert the image to grayscale
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    # Use threshold to convert the grayscale image to binary
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # Use findContours to find the regions of yellow highlight
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    coords = []
    for cnt in contours:
        if cv2.contourArea(cnt) >= min_area:
            x, y, w, h = cv2.boundingRect(cnt)
            coords.append((x, y, x + w, y + h))
    if not len(coords):
        return None
    else:
        return coords[0][:2], coords[0][2:]


if __name__ == '__main__':
    before = 'test/img_3.png'
    after = 'test/img_ed.png'
    top_left, right_bottom = find_highlighted(before, after)

    img = cv2.imread(after)
    cv2.rectangle(img, top_left, right_bottom, (0, 0, 255), 2)
    # Display the result
    cv2.imshow('Result', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
