from flask import Flask, request, jsonify
import os
from stl import mesh
import cadquery as cq
import tempfile

app = Flask(__name__)

# --- STL Volume Calculation ---


def calculate_stl_volume(file_path):
    model = mesh.Mesh.from_file(file_path)
    volume_mm3 = model.get_mass_properties()[0]
    return volume_mm3 / 1000  # convert mm³ to cm³

# --- STEP Volume Calculation ---


def calculate_step_volume(file_path):
    solid = cq.importers.importStep(file_path)
    volume_mm3 = solid.val().Volume()
    return volume_mm3 / 1000  # convert mm³ to cm³

# --- Price Calculation ---


def calculate_price(volume_cm3, rate=0.15, setup_fee=2.0):
    return round(volume_cm3 * rate + setup_fee, 2)

# --- File Upload Endpoint ---


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    ext = os.path.splitext(file.filename)[-1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        if ext == '.stl':
            volume = calculate_stl_volume(tmp_path)
        elif ext in ['.step', '.stp']:
            volume = calculate_step_volume(tmp_path)
        else:
            return jsonify({'error': 'Unsupported file type'}), 400

        price = calculate_price(volume)
        return jsonify({
            'volume_cm3': round(volume, 2),
            'price_eur': price
        })

    finally:
        os.remove(tmp_path)


if __name__ == '__main__':
    app.run(debug=True)
