from flask import Blueprint, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

user_bp = Blueprint('user', __name__)

@user_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400

        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            session['user_id'] = user.id
            return jsonify({'user': user.to_dict()})
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': f'Login failed: {str(e)}'}), 500

@user_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'})

@user_bp.route('/me', methods=['GET'])
def me():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    user = User.query.get(session['user_id'])
    if user:
        return jsonify(user.to_dict())
    else:
        session.pop('user_id', None)
        return jsonify({'error': 'User not found'}), 404

@user_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Username, email and password are required'}), 400

        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 409

        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 409

        user = User(username=data['username'], email=data['email'])
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        return jsonify({'user': user.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500
