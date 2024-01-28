from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import base64
from PIL import Image
from io import BytesIO

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

        processed_image_path = "static/processed_image.jpg"
        if image.filename == '':
            return jsonify({'message': 'No selected file'}), 400

        image.save(processed_image_path)

        return jsonify({"message": "Image uploaded and processed successfully", "image_path": processed_image_path})
    except Exception as e:
        return jsonify({"error": str(e)})



if __name__ == '__main__':
    app.run(debug=True, port=5002)
