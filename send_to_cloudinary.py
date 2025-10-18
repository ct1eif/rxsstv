import json
import os
import time
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name='dqwg2hen7',  # Cloud name correto
    api_key='273725329929199',
    api_secret='z7x9CZLBeg7tlbOf2GsK9inlkUA'
)

UPLOAD_DIR = "/home/pi/qsstv/rx_sstv/"
JSON_FILE = "uploaded_images.json"

while True:
    images = [f for f in os.listdir(UPLOAD_DIR) if f.lower().endswith(('.jpg', '.png'))]
    uploaded = []
    for img_name in images:
        local_path = os.path.join(UPLOAD_DIR, img_name)
        result = cloudinary.uploader.upload(local_path, folder="sstv")
        uploaded.append({"filename": img_name, "url": result['secure_url']})
    # Salva os URLs
    with open(JSON_FILE, "w") as f:
        json.dump(uploaded[-20:], f)  # últimas 20 imagens
    time.sleep(10)



















