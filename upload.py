from flask import Flask, request, jsonify
from PIL import Image, ImageFilter
from io import BytesIO
import base64

app = Flask(__name__)

def apply_averaging_filter(image_bytes):
    img = Image.open(BytesIO(image_bytes))
    filtered = img.filter(ImageFilter.BoxBlur(1))  # 3x3 average kernel equivalent
    buffer = BytesIO()
    filtered.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

@app.route('/api/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    img_data = apply_averaging_filter(file.read())

    return jsonify({'image': img_data})

handler = app  # for Vercel
