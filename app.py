import json
import os
from flask import Flask, render_template, request

app = Flask(__name__)
JSON_FILE = os.path.join(os.getcwd(), "uploaded_images.json")


@app.route('/')
def index():
    images = []
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r') as f:
                images = json.load(f)
        except Exception as e:
            print("Erro a ler JSON:", e)
            images = []
    return render_template('index.html', images=images)


# NOVO ENDPOINT para receber updates do Raspberry Pi
@app.route('/update_images', methods=['POST'])
def update_images():
    token = request.headers.get('Authorization')
    if token != os.environ.get('UPDATE_TOKEN'):
        return "Unauthorized", 401

    data = request.get_json()
    if not data or 'images' not in data:
        return "Bad Request: no images field", 400

    try:
        with open(JSON_FILE, 'w') as f:
            json.dump(data['images'], f)
        print("Recebido update com", len(data['images']), "imagens.")
        return {"status": "ok"}, 200
    except Exception as e:
        print("Erro ao gravar JSON:", e)
        return {"status": "error", "message": str(e)}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
