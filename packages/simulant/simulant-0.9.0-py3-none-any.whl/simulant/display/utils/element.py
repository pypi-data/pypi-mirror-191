import cv2
import numpy
import numpy as np


# screenshot_img = numpy.array(screanshot_img_path)[:, :, ::-1].copy()


# def find_element(template_img_path, screanshot_img_path):
#     # Load the screenshot image
#     screenshot_img = numpy.array(screanshot_img_path)[:, :, ::-1].copy()
#     # screenshot_img = cv2.imread(screanshot_img_path)
#     # Load the template image to search for
#     template_img = cv2.imread(template_img_path)
#     # Perform matchTemplate to get the matching result
#     result = cv2.matchTemplate(screenshot_img, template_img, cv2.TM_CCOEFF_NORMED)
#     # Get the coordinates of the best match
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
#     # Draw a rectangle on the screenshot to highlight the match
#     top_left = max_loc
#     bottom_right = (top_left[0] + template_img.shape[1], top_left[1] + template_img.shape[0])
#     return top_left, bottom_right
#
#
# def find_element_tmp(template_img_path, screanshot_img_path, threshold):
#     # Load the screenshot image
#     screenshot_img = numpy.array(screanshot_img_path)[:, :, ::-1].copy()
#     # screenshot_img = cv2.imread(screanshot_img_path)
#     # Load the template image to search for
#     template_img = cv2.imread(template_img_path)
#     # Perform matchTemplate to get the matching result
#     result = cv2.matchTemplate(screenshot_img, template_img, cv2.TM_CCOEFF_NORMED)
#     # Get all the locations where the template matches the screenshot above the threshold
#     locs = numpy.where(result >= threshold)
#     # Get the coordinates of the best match
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
#     # Draw a rectangle on the screenshot to highlight the match
#     coords = list(zip(*locs[::-1]))
#     return coords
#

def find_element(template_img_path, screenshot_img, threshold=.8):
    # Load the screenshot image
    screenshot_img = numpy.array(screenshot_img)[:, :, ::-1].copy()
    # Load the template image to search for
    template_img = cv2.imread(template_img_path)
    # Perform matchTemplate to get the matching result
    result = cv2.matchTemplate(screenshot_img, template_img, cv2.TM_CCOEFF_NORMED)
    # Set the threshold for finding matches
    matches = np.where(result >= threshold)
    # Create an empty list to store the coordinates of matches
    coords = []
    for match in zip(*matches[::-1]):
        coords.append((match[0], match[1], match[0] + template_img.shape[1], match[1] + template_img.shape[0]))
    if coords:
        return coords[0][:2], coords[0][2:]
    return


def find_elements(template_img_path, screanshot_img_path, threshold=.8):
    # Load the screenshot image
    screenshot_img = numpy.array(screanshot_img_path)[:, :, ::-1].copy()
    # screenshot_img = cv2.imread(screanshot_img_path)
    # Load the template image to search for
    template_img = cv2.imread(template_img_path)
    # Perform matchTemplate to get the matching result
    result = cv2.matchTemplate(screenshot_img, template_img, cv2.TM_CCOEFF_NORMED)
    # Find all the matches in the screenshot
    matches = np.where(result >= threshold)
    # Store the coordinates of all the matches in an array
    coordinates = np.column_stack((matches[1], matches[0]))
    return coordinates


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
