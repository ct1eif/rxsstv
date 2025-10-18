import os
import requests

# Caminho local onde o QSSTV guarda as imagens
IMAGE_DIR = "/home/pi/qsstv/rx_sstv/"

# URL do teu app Render
UPLOAD_URL = "https://rxsstv.onrender.com/upload"
API_KEY = "ct1eif2025"  # mesma chave definida no Render

for filename in os.listdir(IMAGE_DIR):
    if filename.lower().endswith(('.jpg', '.png')):
        filepath = os.path.join(IMAGE_DIR, filename)
        with open(filepath, 'rb') as f:
            files = {'file': f}
            headers = {'Authorization': API_KEY}
            try:
                r = requests.post(UPLOAD_URL, files=files, headers=headers)
                print(f"Enviando {filename} -> {r.status_code} {r.text}")
            except Exception as e:
                print(f"Erro ao enviar {filename}: {e}")
