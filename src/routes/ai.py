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

        # Получаем модель из запроса, по умолчанию используем GLM
        model = data.get('model', 'z-ai/glm-4.5-air:free')

        # Ключ для контекста в сессии
        context_key = f'context_{model}'

        # Инициализируем контекст если не существует
        if context_key not in session:
            session[context_key] = []

        context = session[context_key]

        # Добавляем пользовательское сообщение в контекст
        context.append({'role': 'user', 'content': data['message']})

        # Ограничиваем контекст 10 сообщениями (5 пар user-assistant)
        if len(context) > 10:
            # Сбрасываем контекст и добавляем уведомление
            context = [{'role': 'assistant', 'content': 'Контекст был сброшен из-за превышения лимита в 10 сообщений. Начинаем новый разговор.'}]
            context.append({'role': 'user', 'content': data['message']})
            session[context_key] = context

        # Получаем API ключ из переменных окружения
        api_key = os.getenv('DEEPSEEK_API_KEY')

        if not api_key:
            return jsonify({'error': 'AI service not configured'}), 500

        # Запрос к OpenRouter API
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://your-app-domain.com',
            'X-Title': 'Business Analytics App'
        }

        # Сообщения для API: system + context
        messages = [
            {
                'role': 'system',
                'content': 'You are a business analytics assistant. Help users with data analysis, market research, business strategy, and insights. Provide clear, actionable recommendations.'
            }
        ] + context

        payload = {
            'model': model,
            'messages': messages,
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

            # Добавляем ответ AI в контекст
            context.append({'role': 'assistant', 'content': ai_response})
            session[context_key] = context

            # Возвращаем ответ и статус контекста
            context_count = len([msg for msg in context if msg['role'] == 'user'])
            return jsonify({
                'response': ai_response,
                'context_status': f'Контекст: {context_count}/10 сообщений'
            })
        else:
            return jsonify({'error': f'AI service error: {response.status_code}'}), 500

    except requests.exceptions.Timeout:
        return jsonify({'error': 'AI service timeout'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'AI service request failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal error: {str(e)}'}), 500

@ai_bp.route('/context/status', methods=['GET'])
@login_required
def get_context_status():
    model = request.args.get('model', 'z-ai/glm-4.5-air:free')
    context_key = f'context_{model}'

    if context_key not in session:
        return jsonify({'status': 'Контекст: 0/10 сообщений'})

    context = session[context_key]
    context_count = len([msg for msg in context if msg['role'] == 'user'])
    return jsonify({'status': f'Контекст: {context_count}/10 сообщений'})

@ai_bp.route('/context/reset', methods=['POST'])
@login_required
def reset_context():
    data = request.json or {}
    model = data.get('model', 'z-ai/glm-4.5-air:free')
    context_key = f'context_{model}'

    session[context_key] = []
    return jsonify({'message': 'Контекст сброшен', 'status': 'Контекст: 0/10 сообщений'})
