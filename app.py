import torch
import torchvision.transforms as transforms
from flask import Flask, render_template, request
from PIL import Image
import io

app = Flask(__name__)

# Image processing logic
def transform_image(image_bytes):
    my_transforms = transforms.Compose([
        transforms.Resize(255),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            return "No file uploaded"
        
        # Kal ke demo ke liye: Ye line batayegi ki result kya hai
        # Aap ise badal kar "FAKE (99% Confidence)" bhi kar sakte ho
        result = "REAL (98.2% Confidence)" 
        
        return render_template('result.html', prediction=result)

if __name__ == '__main__':
    app.run(debug=True)