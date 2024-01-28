import os
import torch
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
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
        if (type(image_array) == int):
            return (None, None)
        else:
            image_array = image_array.flatten()

        bw_pil_image = torch.tensor(bw_pil_image, dtype=torch.float32)
        bw_pil_image = bw_pil_image.unsqueeze(0)
        # print("---------------------- PIL IMAGE ----------------------")
        # print(bw_pil_image.shape)

            # You can apply transformations to bw_cv2_array if needed

        # print(type(bw_pil_image), bw_pil_image)
        # print(type(image_array), image_array)

        return (bw_pil_image, image_array)
    
def dataload_create(image_folder_path):
    custom_dataset = CustomDataset(image_folder_path)
    # print(len(custom_dataset))
    train_dataset, test_dataset = torch.utils.data.random_split(custom_dataset, [1000, 1]) # 80% train, 20% test
    # print(len(train_dataset))
    # print(len(test_dataset))
    train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_dataloader = DataLoader(test_dataset, batch_size=32, shuffle=True)
    return train_dataloader, test_dataloader

if __name__ == "__main__":
    train, test = dataload_create("../images")
    for i, (bw_pil_image, image_array) in enumerate(train):
        print(i, bw_pil_image.shape, image_array.shape)
        print(bw_pil_image)
        if i == 20:
            break