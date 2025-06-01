from flask import send_from_directory
from flask import Flask, request, render_template, jsonify
import os
import trimesh


from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.BRepGProp import brepgprop_VolumeProperties
from OCC.Core.GProp import GProp_GProps
from OCC.Core.TopAbs import TopAbs_SOLID
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import topods_Solid


def calculate_step_volume(filepath):
    try:
        # Load the STEP file - zkouška, jestli lze načíst STEP soubor
        step_reader = STEPControl_Reader()
        status = step_reader.ReadFile(filepath)

        if status != IFSelect_RetDone:
            raise Exception("Failed to read STEP file.")

        # Transfer all roots to shape
        step_reader.TransferRoots()
        shape = step_reader.OneShape()

        # Calculate volume for all solids
        exp = TopExp_Explorer(shape, TopAbs_SOLID)
        total_volume = 0.0

        while exp.More():
            solid = topods_Solid(exp.Current())
            props = GProp_GProps()
            brepgprop_VolumeProperties(solid, props)
            total_volume += props.Mass()
            exp.Next()

        return total_volume / 1000  # Convert mm³ to cm³

    except Exception as e:
        raise Exception(f"Error reading STEP file: {str(e)}")


app = Flask(__name__)


@app.route('/uploads/<path:filename>')
def serve_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, mimetype=mimetype)


UPLOAD_FOLDER = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'uploads')

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

        print(f"Saved file to: {filename}")
        print(f"File exists? {os.path.exists(filename)}")

        try:
            ext = file.filename.rsplit('.', 1)[1].lower()

            if ext in ['step', 'stp']:
                volume = calculate_step_volume(filename)
            elif ext == 'stl':
                mesh = trimesh.load_mesh(filename)
                volume = mesh.volume / 1000  # Convert mm³ to cm³

            else:
                return jsonify({"error": "Unsupported file type"}), 400

            price = volume * 2.9  # Simple pricing logic
            return jsonify({"volume": volume, "price": price})

        except Exception as e:
            return jsonify({"error": f"Error processing the 3D model: {str(e)}"}), 500

    return jsonify({"error": "Invalid file type"}), 400


if __name__ == "__main__":
    # For local development (this is optional)
    app.run(debug=True, host="0.0.0.0", port=5000)
