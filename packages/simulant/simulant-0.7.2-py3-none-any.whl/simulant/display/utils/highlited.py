import cv2


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
