import os
from PIL import Image
import numpy as np
# from . import landmark_utils
import landmark_utils


def resize_and_convert_to_bw_both(input_path):
    # Open the image using Pillow
    pil_image = Image.open(input_path)

    # Resize the image to 256x256 pixels using Pillow
    resized_pil_image = pil_image.resize((256, 256))

    # Convert the Pillow image to black and white
    bw_pil_image = resized_pil_image.convert("L")

    # Normalize the image
    bw_pil_image = np.array(bw_pil_image, dtype=np.float32) / 255.0
    
    return bw_pil_image

# get the list of image file names
image_folder_path = "images"
image_files = os.listdir(image_folder_path)
for idx in range(len(image_files)):
    # Load image and features
    image_path = os.path.join(image_folder_path, image_files[idx])
    bw_pil_image = resize_and_convert_to_bw_both(image_path)
    # Convert image to a numpy array
    image_array = landmark_utils.generate_landmarks(image_path)
    if (type(image_array) == int):
        # print("ERROR: LANDMARK NOT DETECTED")
        # move the image to another folder
        os.rename(image_path, "discarded_images/" + image_files[idx])
    else:
        # print("LANDMARK DETECTED")
        pass