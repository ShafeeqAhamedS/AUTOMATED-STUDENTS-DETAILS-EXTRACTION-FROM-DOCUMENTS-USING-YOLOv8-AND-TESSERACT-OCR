from flask import Flask, render_template, request, jsonify
from PIL import Image
from pdf2image import convert_from_path
from ultralytics import YOLO
from IPython.display import display, Image
import cv2
import os
import pytesseract
os.environ['PATH'] += r'C:\ProgramFiles\Tesseract-OCR'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import os
import time  # Add time module for demonstration

app = Flask(__name__)

model = YOLO("./runs/detect/train_medium_final/weights/best.pt")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Collect input from the user
        name = request.form['name']
        dept = request.form['dept']
        batch = request.form['batch']
        reg_number = request.form['reg_number']
        file = request.files['photo']

        # Save the uploaded file (10th Marksheet)
        allowed_extensions = {'png', 'jpg', 'jpeg'}
        if file.filename.lower().split('.')[-1] not in allowed_extensions:
            return jsonify({'error': 'Invalid file type. Please upload a valid image file.'})

        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        img = cv2.imread(file_path)
        results = model.predict(img)

        sizes,classes,text = [],[],[]
        for r in results:
            for id in range(0, len(r)):
                x, y, x1, y1 = r.boxes.xyxy.cpu().numpy().astype(int)[id]
                sizes.extend([[y,y1,x,x1]])
                classes.append(r.names[r.boxes.cls.cpu().numpy()[id]])

        for c in range(0,len(classes)):
            roi = img[sizes[c][0]:sizes[c][1], sizes[c][2]:sizes[c][3]]
            gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            extracted_text = pytesseract.image_to_string(gray_roi, lang='eng',
                                    config='--psm 10 --oem 3 -c tessedit_char_whitelist=" QWERTYUIOPASDFGHJKLZXCVBNM,."')
            text.append(extracted_text)
        # For demonstration purposes, simulate a delay (replace with actual model inference)
        time.sleep(2)

        # Return the extracted text and image path as JSON
        return jsonify({'predicted_texts': text})

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)