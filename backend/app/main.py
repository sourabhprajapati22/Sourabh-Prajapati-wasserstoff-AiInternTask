from flask import Flask, render_template
from app.api.routes import api_bp
from app.config import Config
import os
from app.services.embedding_monitor import run_embedding_monitor
import threading
import multiprocessing

def start_background_embedding(upload_folder):
    try:
        # Try multiprocessing first
        p = multiprocessing.Process(target=run_embedding_monitor, args=(upload_folder,))
        p.daemon = True
        p.start()
        print("🚀 Embedding monitor started using multiprocessing.")
    except (ImportError, RuntimeError, OSError) as e:
        print(f"⚠️ Multiprocessing failed ({e}), falling back to threading.")
        t = threading.Thread(target=run_embedding_monitor, args=(upload_folder,), daemon=True)
        t.start()
        print("🚀 Embedding monitor started using threading.")

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def home():
        return render_template('index.html')

    # Start background task
    start_background_embedding(app.config['UPLOAD_FOLDER'])

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)