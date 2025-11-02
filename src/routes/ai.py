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

        # Запрос к OpenRouter API (маршрутизация через OpenRouter)
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://your-app-domain.com',  # Замените на ваш домен
            'X-Title': 'Business Analytics App'
        }

        payload = {
            'model': 'z-ai/glm-4.5-air:free',  # OpenRouter формат модели
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are a business analytics assistant. Help users with data analysis, market research, business strategy, and insights. Provide clear, actionable recommendations.'
                },
                {
                    'role': 'user',
                    'content': data['message']
                }
            ],
            'max_tokens': 1000,
            'temperature': 0.7
        }

        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            return jsonify({'response': ai_response})
        else:
            return jsonify({'error': f'AI service error: {response.status_code}'}), 500

    except requests.exceptions.Timeout:
        return jsonify({'error': 'AI service timeout'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'AI service request failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal error: {str(e)}'}), 500
