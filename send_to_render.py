import requests
import os
import time

API_KEY = "UPLOAD_API_KEY"  # mesma chave definida no Render
UPLOAD_URL = "https://rxsstv.onrender.com/upload"  # URL do teu app no Render
IMAGE_DIR = "/home/pi/qsstv/rx_sstv/"  # pasta local do QSSTV

sent_files = set()

while True:
    files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.jpg','.png'))]
    for f in files:
        if f in sent_files:
            continue  # já foi enviado

        file_path = os.path.join(IMAGE_DIR, f)
        try:
            with open(file_path, 'rb') as img:
                response = requests.post(
                    UPLOAD_URL,
                    headers={"Authorization": API_KEY},
                    files={"file": img}
                )
            if response.status_code == 200:
                print(f"✅ Enviado {f}")
                sent_files.add(f)
            else:
                print(f"❌ Falha enviar {f} -> {response.status_code} {response.text}")
        except Exception as e:
            print(f"⚠️ Erro ao enviar {f}: {e}")
    time.sleep(30)  # verifica a cada 30 segundos
