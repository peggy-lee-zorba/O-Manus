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
        api_key = 'sk-'
        
        if not api_key:
            return jsonify({'error': 'AI service not configured'}), 500
        
        # Подготавливаем запрос к Deepseek API
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': data.get('model', 'deepseek-chat'),
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are a helpful business analytics assistant. Provide insights, analysis, and recommendations for business-related questions.'
                },
                {
                    'role': 'user',
                    'content': data['message']
                }
            ],
            'max_tokens': data.get('max_tokens', 2000),
            'temperature': data.get('temperature', 0.7),
            'stream': False
        }
        
        # Отправляем запрос к Deepseek API
        response = requests.post(
            'https://api.deepseek.com/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            ai_response = response.json()
            return jsonify({
                'success': True,
                'response': ai_response['choices'][0]['message']['content'],
                'usage': ai_response.get('usage', {})
            })
        else:
            return jsonify({
                'error': 'AI service error',
                'details': response.text
            }), response.status_code
            
    except requests.exceptions.Timeout:
        return jsonify({'error': 'AI service timeout'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Network error: {str(e)}'}), 503
    except Exception as e:
        return jsonify({'error': f'Internal error: {str(e)}'}), 500

@ai_bp.route('/models', methods=['GET'])
@login_required
def get_models():
    """Возвращает список доступных моделей"""
    models = [
        {
            'id': 'deepseek-chat',
            'name': 'DeepSeek Chat',
            'description': 'DeepSeek-V3.1 non-thinking mode for general conversations'
        },
        {
            'id': 'deepseek-reasoner',
            'name': 'DeepSeek Reasoner',
            'description': 'DeepSeek-V3.1 thinking mode for complex reasoning tasks'
        }
    ]
    return jsonify({'models': models})

@ai_bp.route('/status', methods=['GET'])
@login_required
def get_status():
    """Проверяет статус AI сервиса"""
    api_key = 'sk-'
    
    if not api_key:
        return jsonify({
            'status': 'error',
            'message': 'DEEPSEEK_API_KEY not configured'
        }), 500
    
    try:
        # Простой тестовый запрос для проверки API
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        
        payload = {
            'model': 'deepseek-chat',
            'messages': [{'role': 'user', 'content': 'test'}],
            'max_tokens': 1,
            'stream': False
        }
        
        response = requests.post(
            'https://api.deepseek.com/chat/completions',
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return jsonify({
                'status': 'ok',
                'message': 'DeepSeek API is working'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': f'API error: {response.status_code}'
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Connection error: {str(e)}'
        }), 500



