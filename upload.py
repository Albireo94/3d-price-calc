import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder='templates')

UPLOAD_FOLDER = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    # properly serves templates/index.html
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print(f"Saved file to: {filepath}")
        return jsonify(price=123.45)  # Replace with real logic
    return jsonify(error="No file received"), 400


if __name__ == '__main__':
    app.run(debug=True)
