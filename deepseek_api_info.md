# Deepseek API Integration Information

## API Configuration
- **Base URL**: `https://api.deepseek.com` (или `https://api.deepseek.com/v1` для совместимости с OpenAI)
- **API Key**: Требуется получить на платформе Deepseek
- **Формат**: Совместим с OpenAI API

## Доступные модели
- **deepseek-chat**: Режим без размышлений (non-thinking mode) DeepSeek-V3.1
- **deepseek-reasoner**: Режим с размышлениями (thinking mode) DeepSeek-V3.1

## Пример запроса (curl)
```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <DeepSeek API Key>" \
  -d '{
        "model": "deepseek-chat",
        "messages": [
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "Hello!"}
        ],
        "stream": false
      }'
```

## Пример для Python (OpenAI SDK)
```python
from openai import OpenAI

client = OpenAI(
    api_key="<DeepSeek API Key>",
    base_url="https://api.deepseek.com"
)

completion = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    stream=False
)
```

## Интеграция в наш проект
Нужно модифицировать файл `/home/ubuntu/ai-proxy/src/routes/ai.py`:
1. Изменить `base_url` на `https://api.deepseek.com`
2. Использовать переменную окружения `DEEPSEEK_API_KEY` вместо `OPENAI_API_KEY`
3. Установить модель по умолчанию как `deepseek-chat`

