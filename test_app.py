#!/usr/bin/env python3

try:
    from flask import Flask
    from flask_cors import CORS
    from flask_sqlalchemy import SQLAlchemy

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app, supports_credentials=True)

    # Initialize database
    db = SQLAlchemy()

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password_hash = db.Column(db.String(255), nullable=False)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        print("✓ Database initialized successfully")

    print("✓ Flask app created successfully")

except Exception as e:
    print(f"✗ Error creating Flask app: {e}")
    import traceback
    traceback.print_exc()

print("App creation test completed.")
