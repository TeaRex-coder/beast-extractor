from flask import Flask, request, send_file, jsonify
from files import processUploadedZip
import tempfile

app = Flask(__name__)


@app.route("/process-zip", methods=["POST"])
def handle_zip_processing():
    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400

    uploaded_file = request.files["file"]

    if uploaded_file.filename == "":
        return jsonify({"error": "no file"}), 400

    if not uploaded_file.filename.lower().endswith(".zip"):
        return jsonify({"error": "file isn's a ZIP"}), 400

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            result_path = processUploadedZip(uploaded_file, temp_dir)
            return send_file(
                result_path,
                as_attachment=True,
                download_name="output.zip",
                mimetype="application/zip",
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=False)
