# Business Analytics App

AI-powered business analytics platform with DeepSeek integration.

## Setup

1. Clone the repository
2. Install Python dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and configure your environment variables
4. Run: `python main.py`

## Environment Variables

Create a `.env` file in the root directory (copy from `.env.example`):

```
SECRET_KEY=your-secret-key-here
DEEPSEEK_API_KEY=your-openrouter-api-key-here
FLASK_DEBUG=True
```

## Features

- **User Authentication**: Login/logout system with session management
- **AI Chat**: Business analytics assistant powered by DeepSeek AI
- **Modern UI**: Responsive React interface with Tailwind CSS
- **Database**: SQLite database with SQLAlchemy ORM

## API Endpoints

- `POST /api/login` - User login
- `POST /api/logout` - User logout
- `GET /api/me` - Get current user info
- `POST /api/register` - Register new user
- `POST /api/chat` - AI chat with business analytics assistant

## Running the Application

```bash
python main.py
```

The application will be available at `http://localhost:5000`

### Default Login Credentials

When you first run the application, a default user is automatically created:

- **Username:** `admin`
- **Password:** `admin123`

You can use these credentials to log in, or register a new account through the application interface.

## Deployment on Render

1. Connect your GitHub repository to Render
2. Add environment variables in Render dashboard
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn main:app`
5. Deploy automatically
