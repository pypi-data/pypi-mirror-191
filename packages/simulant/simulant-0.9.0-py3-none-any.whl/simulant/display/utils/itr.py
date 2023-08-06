import numpy as np
import pytesseract
from PIL import Image


def extract_text(image, top_left=None, bottom_right=None):
    """
    Function to extract text from an image

    Parameters:
        image (PIL.Image.Image or numpy.ndarray): Image.
        top_left (tuple, optional): Tuple of left top coordinates of the bounding box.
        bottom_right (tuple, optional): Tuple of right bottom coordinates of the bounding box.

    Returns:
        str: Extracted text.
    """
    if isinstance(image, Image.Image):
        image = np.array(image)
    if top_left is not None and bottom_right is not None:
        x1, y1 = top_left
        x2, y2 = bottom_right
        roi = image[y1:y2, x1:x2]
    else:
        roi = image
    text = pytesseract.image_to_string(roi)
    return text
