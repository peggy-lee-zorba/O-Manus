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
        
        api_key = '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'
        
        if not api_key:
            return jsonify({'error': 'AI service not configured'}), 500
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://xlhyimcdd0jk.manus.space', # Replace with your actual site URL
            'X-Title': 'Business Analytics Platform', # Replace with your actual site name
        }
        
        payload = {
            'model': data.get('model', 'deepseek/deepseek-chat-v3.1:free'),
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
        
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
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
            'id': 'deepseek/deepseek-chat-v3.1:free',
            'name': 'DeepSeek Chat (OpenRouter)',
            'description': 'DeepSeek-V3.1 non-thinking mode for general conversations via OpenRouter'
        },
        {
            'id': 'deepseek/deepseek-reasoner',
            'name': 'DeepSeek Reasoner (OpenRouter)',
            'description': 'DeepSeek-V3.1 thinking mode for complex reasoning tasks via OpenRouter'
        }
    ]
    return jsonify({'models': models})

@ai_bp.route('/status', methods=['GET'])
@login_required
def get_status():
    """Проверяет статус AI сервиса"""
    api_key = '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'
    
    if not api_key:
        return jsonify({
            'status': 'error',
            'message': 'OpenRouter API Key not configured'
        }), 500
    
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'HTTP-Referer': 'https://xlhyimcdd0jk.manus.space', # Replace with your actual site URL
            'X-Title': 'Business Analytics Platform', # Replace with your actual site name
        }
        
        payload = {
            'model': 'deepseek/deepseek-chat-v3.1:free',
            'messages': [{'role': 'user', 'content': 'test'}],
            'max_tokens': 1,
            'stream': False
        }
        
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return jsonify({
                'status': 'ok',
                'message': 'OpenRouter API is working'
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



