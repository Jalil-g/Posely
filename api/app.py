from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import base64
from PIL import Image
from io import BytesIO
from inference import predict
from data_transformation.landmark_utils import draw_landmarks,  draw_blank_image
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def convert_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode('utf-8')

@app.route('/', methods=['OPTIONS'])
def handle_options():
    response = app.response_class(response="", status=200)
    response.headers['Access-Control-Allow-Origin'] = '*'  # Replace '*' with your frontend URL
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS, POST'
    return response

@app.route('/')
def hello():
    return 'Hello, Flask!'

@app.route('/api/photo', methods=['POST'])
def upload_image():
    try:
        image = request.files['image']

        image_path = "static/image.jpg"
        if image.filename == '':
            return jsonify({'message': 'No selected file'}), 400

        image.save(image_path)
        #scale_image("static/img1.jpeg", image_path)
        prediction, predicted_image = predict(image_path)
        predicted_image_path = os.path.join('..', 'images', predicted_image)
        processed_image_path = 'static/processed_image.jpg'
        #draw_landmarks(predicted_image_path, [], "static/labeled_prediction.jpg")
        draw_blank_image(predicted_image_path)
        # Read the image file
        return jsonify({"labeled": convert_to_base64(processed_image_path), "prediction": convert_to_base64(predicted_image_path), "transparent": convert_to_base64("static/transparent.png")})  #jsonify({"message": "Image uploaded and processed successfully", "image_path": processed_image_path})
    except Exception as e:
        return jsonify({"error": str(e)})



if __name__ == '__main__':
    app.run(debug=True, port=5002)
