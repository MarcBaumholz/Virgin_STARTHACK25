import os
from datetime import timedelta

class Config:
    # Basic Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///virgin_green_hub.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}
    
    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    
    # Security Configuration
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY') or 'csrf-secret-key'
    
    # Rate Limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URL = os.environ.get('RATELIMIT_STORAGE_URL') or 'memory://'
    RATELIMIT_DEFAULT = "200 per day"
    
    # API Configuration
    API_RATE_LIMIT = "100 per minute"
    API_KEY_HEADER = "X-API-Key"
    
    # WebSocket Configuration
    WEBSOCKET_PING_INTERVAL = 30
    WEBSOCKET_PING_TIMEOUT = 10
    
    # Green Points Configuration
    POINTS_PER_ACTION = {
        'project_participation': 10,
        'feedback_submission': 5,
        'idea_submission': 15,
        'idea_implementation': 50
    }
    
    POINTS_PER_LEVEL = {
        1: 0,
        2: 1000,
        3: 2500,
        4: 5000,
        5: 10000,
        6: 20000,
        7: 40000,
        8: 80000,
        9: 160000,
        10: 320000
    }
    
    # Badge Configuration
    BADGES = {
        'early_adopter': {
            'name': 'Early Adopter',
            'description': 'Joined during the first month of launch',
            'points': 500
        },
        'idea_master': {
            'name': 'Idea Master',
            'description': 'Submitted 10 or more ideas',
            'points': 1000
        },
        'community_leader': {
            'name': 'Community Leader',
            'description': 'Received 100 or more votes on ideas',
            'points': 2000
        },
        'project_champion': {
            'name': 'Project Champion',
            'description': 'Participated in 5 or more projects',
            'points': 1500
        },
        'sustainability_expert': {
            'name': 'Sustainability Expert',
            'description': 'Reached level 5',
            'points': 3000
        }
    }
    
    # Project Categories
    PROJECT_CATEGORIES = [
        'Renewable Energy',
        'Waste Reduction',
        'Water Conservation',
        'Carbon Reduction',
        'Sustainable Transportation',
        'Green Building',
        'Biodiversity',
        'Circular Economy',
        'Sustainable Agriculture',
        'Climate Action'
    ]
    
    # Company List
    COMPANIES = [
        'Virgin Airlines',
        'Virgin Trains',
        'Virgin Hotels',
        'Virgin Media',
        'Virgin Money',
        'Virgin Galactic',
        'Virgin Voyages',
        'Virgin Active',
        'Virgin Mobile',
        'Virgin Care'
    ]
    
    # Project Status Options
    PROJECT_STATUS = [
        'Planned',
        'In Progress',
        'Completed',
        'On Hold',
        'Cancelled'
    ]
    
    # Idea Status Options
    IDEA_STATUS = [
        'New',
        'Under Review',
        'Approved',
        'Implemented',
        'Rejected'
    ]
    
    # Chat Room Types
    CHAT_ROOMS = [
        'General Discussion',
        'Best Practices',
        'Expert Sessions',
        'Project Updates',
        'Sustainability News'
    ]
    
    # API Rate Limits
    API_RATE_LIMITS = {
        'standard': {
            'requests_per_minute': 60,
            'requests_per_hour': 1000,
            'requests_per_day': 10000
        },
        'premium': {
            'requests_per_minute': 300,
            'requests_per_hour': 5000,
            'requests_per_day': 50000
        }
    }
    
    # Cache Configuration
    CACHE_TYPE = os.environ.get('CACHE_TYPE') or 'simple'
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'app.log')
    
    # Analytics Configuration
    ANALYTICS_ENABLED = os.environ.get('ANALYTICS_ENABLED', 'True').lower() == 'true'
    ANALYTICS_RETENTION_DAYS = 90
    
    # Feature Flags
    FEATURES = {
        'enable_chat': True,
        'enable_points': True,
        'enable_badges': True,
        'enable_ideas': True,
        'enable_projects': True,
        'enable_api': True,
        'enable_analytics': True,
        'enable_notifications': True
    }

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///virgin_green_hub_dev.db'
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///virgin_green_hub_test.db'
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False
    RATELIMIT_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    WTF_CSRF_ENABLED = True
    RATELIMIT_ENABLED = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 