from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>DeepScan AI is Running!</h1><p>The system is ready for the next task.</p>"

if __name__ == '__main__':
    app.run(debug=True)