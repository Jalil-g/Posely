from PIL import Image
import os
print("Current Working Directcd ory:", os.getcwd())

input_folder = "raw_images"
output_folder = "images"
target_size = (480, 480)  # Set your desired size
print("Starting conversion...")
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):  # Add more extensions if needed
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # Open the image
        image = Image.open(input_path)

        # Resize the image
        resized_image = image.resize(target_size)

        # Convert the image to black and white
        bw_image = resized_image.convert("L")

        # Save the result
        bw_image.save(output_path)

print("Conversion complete.")