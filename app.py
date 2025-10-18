from flask import Flask, request, jsonify, render_template, send_from_directory
import os

app = Flask(__name__)

# Diretório onde as imagens são guardadas
UPLOAD_DIR = os.path.join("static", "rx_sstv")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# A tua chave API
API_KEY = os.environ.get("API_KEY", "ct1eif2025")

@app.route("/")
def index():
    # lista todas as imagens da pasta
    files = sorted(os.listdir(UPLOAD_DIR), reverse=True)
    image_urls = [f"/static/rx_sstv/{f}" for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    return render_template("index.html", images=image_urls)

@app.route("/upload", methods=["POST"])
def upload_file():
    auth = request.headers.get("Authorization")
    if auth != API_KEY:
        return "Unauthorized", 401

    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400

    file = request.files["file"]
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(save_path)
    return jsonify({"filename": file.filename, "status": "ok"})

# Rota opcional para ver lista de imagens em JSON
@app.route("/list")
def list_images():
    files = sorted(os.listdir(UPLOAD_DIR), reverse=True)
    return jsonify(files)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
