import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    API_BASE_URL = 'https://wta-backend.onrender.com/api'
    SESSION_COOKIE_NAME = 'hydro_hubs_session'