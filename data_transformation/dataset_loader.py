import os
import torch
from torch.utils.data import Dataset
from PIL import Image
import numpy as np
from torch.utils.data import DataLoader
import landmark_utils

image_folder_path = "./images"

def resize_and_convert_to_bw_both(input_path):
    # Open the image using Pillow
    pil_image = Image.open(input_path)

    # Resize the image to 480x480 pixels using Pillow
    resized_pil_image = pil_image.resize((256, 256))

    # Convert the Pillow image to black and white
    bw_pil_image = resized_pil_image.convert("L")
    
    return bw_pil_image

class CustomDataset(Dataset):
    def __init__(self, image_folder_path, transform=None):
        self.image_folder_path = image_folder_path
        self.transform = transform

        # Get the list of image file names
        self.image_files = os.listdir(image_folder_path)

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        # Load image and features
        image_path = os.path.join(self.image_folder_path, self.image_files[idx])
        bw_pil_image = resize_and_convert_to_bw_both(image_path)

        # Convert image to a numpy array
        image_array = landmark_utils.generate_landmarks(image_path)

        # Apply transformations if provided
        if self.transform:
            bw_pil_image = self.transform(bw_pil_image)
            # You can apply transformations to bw_cv2_array if needed

        return bw_pil_image, image_array

custom_dataset = CustomDataset(image_folder_path)
print(len(custom_dataset))
train_dataset, test_dataset = torch.utils.data.random_split(custom_dataset, [800, 201]) # 80% train, 20% test
print(len(train_dataset))
print(len(test_dataset))

train_dataloader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=64, shuffle=True)