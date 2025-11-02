#!/usr/bin/env python3

try:
    import flask
    print("✓ Flask imported successfully")
except ImportError as e:
    print(f"✗ Flask import failed: {e}")

try:
    import flask_cors
    print("✓ Flask-CORS imported successfully")
except ImportError as e:
    print(f"✗ Flask-CORS import failed: {e}")

try:
    import flask_sqlalchemy
    print("✓ Flask-SQLAlchemy imported successfully")
except ImportError as e:
    print(f"✗ Flask-SQLAlchemy import failed: {e}")

try:
    import requests
    print("✓ Requests imported successfully")
except ImportError as e:
    print(f"✗ Requests import failed: {e}")

try:
    from src.routes.user import db, User
    print("✓ User model imported successfully")
except ImportError as e:
    print(f"✗ User model import failed: {e}")

try:
    from src.routes.ai import ai_bp
    print("✓ AI blueprint imported successfully")
except ImportError as e:
    print(f"✗ AI blueprint import failed: {e}")

print("Import test completed.")
