from PIL import Image
import cv2
import numpy as np

def resize_and_convert_to_bw_both(input_path):
    # Open the image using Pillow
    pil_image = Image.open(input_path)

    # Resize the image to 480x480 pixels using Pillow
    resized_pil_image = pil_image.resize((480, 480))

    # Convert the Pillow image to black and white
    bw_pil_image = resized_pil_image.convert("L")

    # Convert the Pillow image to a NumPy array for OpenCV
    cv2_array = np.array(resized_pil_image)

    # Resize the NumPy array to 480x480 pixels using OpenCV
    resized_cv2_array = cv2.resize(cv2_array, (480, 480))

    # Convert the OpenCV array to grayscale
    bw_cv2_array = cv2.cvtColor(resized_cv2_array, cv2.COLOR_BGR2GRAY)

    return bw_pil_image, bw_cv2_array