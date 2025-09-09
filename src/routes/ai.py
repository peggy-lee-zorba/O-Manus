from flask import Blueprint, jsonify, request, session
import requests
import os
from functools import wraps

ai_bp = Blueprint('ai', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

@ai_bp.route('/chat', methods=['POST'])
@login_required
def chat():
    try:
        data = request.json
        
        if not data or not data.get('message'):
            return jsonify({'error': 'Message is required'}), 400
        
        # Получаем API ключ из переменных окружения
        api_key = os.getenv('DEEPSEEK_API_KEY')
        
        if not api_key:
            return jsonify({'error': 'AI service not configured'}), 500
        
        # Остальной код без изменений...
        # [Сохраняем логику запроса к DeepSeek API]
        
    except Exception as e:
        return jsonify({'error': f'Internal error: {str(e)}'}), 500

# Остальные маршруты без изменений...