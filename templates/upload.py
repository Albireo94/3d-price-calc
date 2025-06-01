from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')  # serve your HTML


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    # Simulate a calculated price — you can replace with real logic later
    return jsonify(price=12312312.45)


if __name__ == '__main__':
    app.run(debug=True)
