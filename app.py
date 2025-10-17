from flask import Flask, render_template, send_from_directory, request, abort
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Diretório local onde o QSSTV guarda as imagens
IMAGE_DIR = "/home/pi/qsstv/rx_sstv/"

# Extensões de imagem permitidas
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)

    images = sorted(
        [f for f in os.listdir(IMAGE_DIR) if allowed_file(f)],
        key=lambda x: os.path.getmtime(os.path.join(IMAGE_DIR, x)),
        reverse=True
    )[:20]  # Mostra apenas as 20 mais recentes

    image_data = []
    for img in images:
        name = os.path.splitext(img)[0]
        parts = name.split('_')
        if len(parts) >= 3:
            mode = parts[0]
            dt_raw = ''.join(parts[1:])
            datetime = (f"{dt_raw[:4]}-{dt_raw[4:6]}-{dt_raw[6:8]} "
                        f"{dt_raw[8:10]}:{dt_raw[10:12]}:{dt_raw[12:14]}")
        else:
            mode = "Desconhecido"
            datetime = "Desconhecida"

        band = "20m Band"
        image_data.append({"filename": img, "mode": mode, "datetime": datetime, "band": band})

    return render_template('index.html', images=image_data)

# Serve as imagens diretamente da pasta QSSTV
@app.route('/rx_sstv/<filename>')
def rx_sstv(filename):
    return send_from_directory(IMAGE_DIR, filename)

# Endpoint para upload externo (Render)
@app.route('/upload', methods=['POST'])
def upload():
    api_key = request.headers.get('X-API-KEY') or request.args.get('api_key')
    if api_key != os.environ.get('UPLOAD_API_KEY'):
        abort(401)

    if 'file' not in request.files:
        return "No file", 400

    file = request.files['file']
    if file.filename == '':
        return "Empty filename", 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        dest = os.path.join(IMAGE_DIR, filename)
        file.save(dest)
        return "OK", 200

    return "Invalid file", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
