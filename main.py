import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='src/static')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app, supports_credentials=True)

# Initialize database
from src.routes.user import db
db.init_app(app)

# Create tables and default user
with app.app_context():
    db.create_all()

    # Create default user if none exists
    from src.routes.user import User
    if not User.query.first():
        default_user = User(username='testuser', email='testuser@example.com')
        default_user.set_password('testuser2025')
        db.session.add(default_user)
        db.session.commit()
        print("✓ Default user created: testuser / testuser2025")

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
