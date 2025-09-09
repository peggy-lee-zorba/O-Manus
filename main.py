import os
from flask import Flask, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='src/static')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

CORS(app, supports_credentials=True)

# Регистрация маршрутов
from src.routes.user import user_bp
from src.routes.ai import ai_bp
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(ai_bp, url_prefix='/api')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_DEBUG', False))