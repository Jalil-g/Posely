from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import base64
from PIL import Image
from io import BytesIO
from data_transformation.landmark_utils import scale_image, draw_landmarks

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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
        draw_landmarks("static/img1.jpeg")

        processed_image_path = 'static/processed_image.jpg'
        # Read the image file
        with open(processed_image_path, 'rb') as image_file:
            image_data = image_file.read()

        # Convert the image data to base64
        base64_image = base64.b64encode(image_data).decode('utf-8')
        print(base64_image[:10])
        return jsonify({"base64": base64_image})  #jsonify({"message": "Image uploaded and processed successfully", "image_path": processed_image_path})
    except Exception as e:
        return jsonify({"error": str(e)})



if __name__ == '__main__':
    app.run(debug=True, port=5002)
