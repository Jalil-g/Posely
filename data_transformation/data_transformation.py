import cv2

def resize_and_convert_to_bw_cv2(input_path):
    # Read the image using OpenCV
    original_image = cv2.imread(input_path)

    # Resize the image to 480x480 pixels
    resized_image = cv2.resize(original_image, (480, 480))

    # Convert the image to grayscale
    bw_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    return bw_image