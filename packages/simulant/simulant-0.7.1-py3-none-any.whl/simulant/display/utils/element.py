import cv2


def find_element(template_img_path, screanshot_img_path):
    # Load the screenshot image
    screenshot_img = cv2.imread(screanshot_img_path)
    # Load the template image to search for
    template_img = cv2.imread(template_img_path)
    # Perform matchTemplate to get the matching result
    result = cv2.matchTemplate(screenshot_img, template_img, cv2.TM_CCOEFF_NORMED)
    # Get the coordinates of the best match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # Draw a rectangle on the screenshot to highlight the match
    top_left = max_loc
    bottom_right = (top_left[0] + template_img.shape[1], top_left[1] + template_img.shape[0])
    return top_left, bottom_right


if __name__ == '__main__':
    template = 'test/img_1.png'
    screanshot = 'test/img.png'
    top, bottom = find_element(template, screanshot)

    screenshot = cv2.imread(screanshot)
    cv2.rectangle(screenshot, top, bottom, (0, 0, 255), 2)
    # Display the result
    cv2.imshow('Result', screenshot)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
