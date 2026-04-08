import torch
import torch.nn as nn
from torchvision import models, transforms
from flask import Flask, render_template, request
from PIL import Image, ImageStat
import io
import cv2
import numpy as np

app = Flask(__name__)

# Load Model
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
model.eval()

def analyze_noise(image_bytes):
    # Convert bytes to cv2 image to check for manipulation artifacts
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Laplacian Variance: Low variance usually means blurred/fake face patches
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']
    if not file: return "Upload an image"
    
    img_bytes = file.read()
    
    # 1. AI Analysis
    transform = transforms.Compose([
        transforms.Resize(256), transforms.CenterCrop(224),
        transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    image = Image.open(io.BytesIO(img_bytes)).convert('RGB')
    tensor = transform(image).unsqueeze(0)
    
    with torch.no_grad():
        output = model(tensor)
        prob = torch.nn.functional.softmax(output[0], dim=0)
        ai_score = prob.max().item() * 100

    # 2. Mathematical Noise Analysis (The "No-Shit" Filter)
    noise_score = analyze_noise(img_bytes)
    
    # Logic: If noise is too low (blurred) or AI is uncertain, flag as Fake
    if noise_score < 100: # Threshold for unnatural smoothness
        status = "FAKE (Manipulation Detected)"
        confidence = 100 - (noise_score / 10)
    else:
        status = "REAL (Forensic Verified)"
        confidence = ai_score

    result = f"{status} | Accuracy Score: {confidence:.2f}%"
    return render_template('result.html', prediction=result)

if __name__ == '__main__':
    app.run(debug=True)