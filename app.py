import torch
import torchvision.transforms as transforms
from flask import Flask, render_template, request
from PIL import Image
import io

app = Flask(__name__)

# Step 1: Image ko AI ke samajhne layak banana
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

# Step 2: Photo upload hone par kya hoga
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            return "No file uploaded"
        
        # Abhi ke liye hum sirf confirmation dikhayenge ki AI ne photo pakad li hai
        return f"<h1>Scan Complete!</h1><p>Image <b>{file.filename}</b> received. AI analysis starting...</p>"

if __name__ == '__main__':
    app.run(debug=True)