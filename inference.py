import torch
import numpy as np
import PIL as Image
from data_transformation.landmark_utils import most_similar_pose, draw_landmarks, generate_pose_array

def predict(model, image_path):
    model.eval()
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

    # TODO: Generate and store poses array in a file
    pose_array = generate_pose_array("data/poses")

    most_similar = most_similar_pose(prediction, pose_array)
    draw_landmarks(image_path, most_similar)
    return prediction, most_similar
