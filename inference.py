import torch
import numpy as np
from PIL import Image
from data_transformation.landmark_utils import most_similar_pose, draw_landmarks, load_pose_array, save_pos_arr, save_name_arr, load_name_array

import torch.nn as nn
from torch.optim import Adam
from data_transformation import dataset_loader
import torch.functional as F
import numpy as np

class PoseAdvisor(nn.Module):
    def __init__(self):
        super(PoseAdvisor, self).__init__()
        self.conv2d = nn.Conv2d(1, 32, (3, 3), padding=1)
        self.pool = nn.MaxPool2d((2, 2), stride=2)
        self.relu = nn.ReLU()
        self.conv2d_1 = nn.Conv2d(32, 64, (3, 3), padding=1)
        self.flatten = nn.Flatten()
        self.linear = nn.Linear(262144, 2056)
        self.linear2 = nn.Linear(2056, 256)
        self.dropout = nn.Dropout(0.2)
        self.linear3 = nn.Linear(256, 39)

    def forward(self, x):
        # print("INPUT", x.shape)
        x = self.conv2d(x)
        x = self.relu(x)
        x = self.pool(x)
        # print("LAYER 1", x.shape)
        x = self.conv2d_1(x)
        x = self.relu(x)
        x = self.pool(x)
        # print("LAYER 2", x.shape)
        x = self.flatten(x)
        x = self.linear(x)
        x = self.relu(x)
        # print("LAYER 3", x.shape)
        x = self.linear2(x)
        x = self.relu(x)
        # print("LAYER 4", x.shape)
        x = self.linear3(x)
        x = self.dropout(x)
        # print("LAYER 5", x.shape)

        return x

model = PoseAdvisor()
model.load_state_dict(torch.load("models/model3.pth"))

def predict(model, image_path):
    # model.eval()
    # Get the image from the image path
    image = Image.open(image_path)

    # Resize the image to 256x256 pixels
    image = image.resize((256, 256))

    # Convert the image to black and white
    image = image.convert("L")

    # Normalize the image
    image = np.array(image, dtype=np.float32) / 255.0

    # Convert image to a PyTorch tensor
    image = image.reshape(1, 1, 256, 256)

    # Add batch dimension to the image
    image = torch.from_numpy(image)
    image = image.float()

    # Get the prediction from the model
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    image = image.to(device)
    model = model.to(device)
    with torch.no_grad():
        prediction = model(image)
        prediction = prediction.cpu().numpy()

    # save_pos_arr("images", "models/pose_arr.npy")
    # save_name_arr("images", "models/name_arr.json")
    pose_array = load_pose_array("models/pose_arr.npy")
    name_array = load_name_array("models/name_arr.json")

    most_similar = most_similar_pose(prediction, pose_array)
    draw_landmarks(image_path, pose_array[most_similar])

    # show the image from the image path
    image_path = name_array[most_similar]
    image = Image.open("images/" + image_path)
    image.show()
    return prediction, most_similar


if __name__ == "__main__":
    print(predict(model, "images/sample_004.jpeg"))