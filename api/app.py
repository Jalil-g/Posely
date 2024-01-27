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
        # Get the base64-encoded image from the request
        print(request.form)
        data_url = request.json['image']
        # Strip the "data:image/jpeg;base64," prefix
        #image_data = data_url.split(",")[1]
        print("test test")
        #print(data_url)

        # Convert base64 to bytes
        image_bytes = base64.b64decode(data_url)
        
        # Create an image from bytes
        img = Image.open(BytesIO(image_bytes))
        
        # Process the image as needed (e.g., resizing, filtering)
        # For demonstration, let's save the processed image
        processed_image_path = "static/processed_image.jpg"
        img.save(processed_image_path)

        return jsonify({"message": "Image uploaded and processed successfully", "image_path": processed_image_path})
    except Exception as e:
        return jsonify({"error": str(e)})



if __name__ == '__main__':
    app.run(debug=True)
