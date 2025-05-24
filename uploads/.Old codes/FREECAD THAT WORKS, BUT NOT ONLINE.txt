from flask import Flask, request, render_template, jsonify
import os
import trimesh

# ✅ NEW: Import FreeCAD only when needed


def calculate_step_volume(filepath):
    try:
        import FreeCAD
        import Part
        shape = Part.Shape()
        shape.read(filepath)
        volume = shape.Volume / 1000  # Convert mm³ to cm³
        return volume
    except Exception as e:
        raise Exception(f"FreeCAD failed: {str(e)}")


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'stl', 'step', 'stp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        try:
            ext = file.filename.rsplit('.', 1)[1].lower()

            # ✅ Use FreeCAD for STEP/STP, Trimesh for STL
            if ext in ['step', 'stp']:
                volume = calculate_step_volume(filename)
            elif ext == 'stl':
                mesh = trimesh.load_mesh(filename)
                volume = mesh.volume
            else:
                return jsonify({"error": "Unsupported file type"}), 400

            price = volume * 0.10  # Simple pricing logic
            return jsonify({"volume": volume, "price": price})

        except Exception as e:
            return jsonify({"error": f"Error processing the 3D model: {str(e)}"}), 500

    return jsonify({"error": "Invalid file type"}), 400


if __name__ == '__main__':
    app.run(debug=True)
