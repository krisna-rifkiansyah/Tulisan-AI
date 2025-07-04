from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import os
import cv2
import numpy as np

def preprocess_image(image_path):
    # Baca gambar
    img = cv2.imread(image_path)

    # Ubah ke grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Penghilangan noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Thresholding (Binarisasi)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Simpan hasil praproses sementara
    processed_path = image_path.replace('.png', '_processed.png').replace('.jpg', '_processed.jpg')
    cv2.imwrite(processed_path, thresh)

    return processed_path

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/api/ocr', methods=['POST'])
def ocr():
    print("request.files:", request.files)
    print("request.form:", request.form)
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Preprocess dulu
    processed_path = preprocess_image(filepath)

    # OCR dari hasil preprocess
    img = Image.open(processed_path)
    text = pytesseract.image_to_string(img, lang='ind')

    # Hapus file sementara
    os.remove(filepath)
    os.remove(processed_path)


    # # OCR
    # img = Image.open(filepath)
    # text = pytesseract.image_to_string(img, lang='ind')  # atau 'ind' untuk Bahasa Indonesia

    # # Hapus file sementara
    # os.remove(filepath)

    return jsonify({'text': text})

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'



