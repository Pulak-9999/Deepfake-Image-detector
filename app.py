from flask import Flask, render_template # <--- Check karo yahan 'render_template' likha hai ya nahi

app = Flask(__name__)

@app.route('/')
def home():
    # Pehle yahan return "DeepScan AI is Running" tha, ab ye likho:
    return render_template('index.html') 

if __name__ == '__main__':
    app.run(debug=True)