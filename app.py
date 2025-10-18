from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# Caminho onde as imagens são guardadas
IMAGE_DIR = "static/rx_sstv"

# Garantir que a pasta existe
os.makedirs(IMAGE_DIR, exist_ok=True)

# Ler chave do ambiente (definida no Render)
UPLOAD_API_KEY = os.environ.get("UPLOAD_API_KEY")

@app.route("/")
def index():
    """Página principal - mostra as imagens guardadas"""
    files = sorted(os.listdir(IMAGE_DIR), reverse=True)
    image_urls = [f"/{IMAGE_DIR}/{f}" for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    return render_template("index.html", image_urls=image_urls)

@app.route("/upload", methods=["POST"])
def upload():
    """Recebe upload via POST"""
    api_key = request.headers.get("Authorization")

    # 🔍 DEBUG - imprime o que o servidor recebeu e o valor esperado (para os logs do Render)
    print("DEBUG: Header Authorization recebido -->", repr(api_key))
    print("DEBUG: UPLOAD_API_KEY (Render) -->", repr(UPLOAD_API_KEY))

    # Aceita tanto "Authorization: Bearer chave" como "Authorization: chave"
    if api_key:
        if api_key.startswith("Bearer "):
            api_key = api_key.split(" ", 1)[1]

    # Valida a chave
    if api_key != UPLOAD_API_KEY:
        print("DEBUG: Chave incorreta. Acesso negado.")
        return "Unauthorized", 401

    # Verifica se há ficheiro
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    # Guarda a imagem na pasta
    save_path = os.path.join(IMAGE_DIR, file.filename)
    file.save(save_path)
    print(f"✅ Upload recebido: {file.filename}")

    return jsonify({"status": "ok", "filename": file.filename})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
