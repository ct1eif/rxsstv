from flask import Flask, render_template
import cloudinary
import cloudinary.api

app = Flask(__name__)

# Configura Cloudinary
cloudinary.config(
    cloud_name='dqwg2hen7',
    api_key='273725329929199',
    api_secret='z7x9CZLBeg7tlbOf2GsK9inlkUA'
)

@app.route('/')
def index():
    try:
        # Lista imagens do folder 'sstv', ordenadas por data
        res = cloudinary.api.resources(type='upload', prefix='sstv', max_results=20, direction='desc')
        images = [img['secure_url'] for img in res['resources']]
    except Exception as e:
        print(f"Erro ao listar imagens: {e}")
        images = []
    return render_template('index.html', images=images)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
