import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "replace-with-your-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///mechanic_shop.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300
    RATELIMIT_STORAGE_URI = "memory://"
    RATELIMIT_DEFAULT = "200/day;50/hour"
    SWAGGER_HOST = os.getenv("SWAGGER_HOST", "127.0.0.1:5000")
    SWAGGER_SCHEMES = ["http"]


class ProductionConfig(Config):
    SWAGGER_HOST = os.getenv("SWAGGER_HOST", "your-render-service.onrender.com")
    SWAGGER_SCHEMES = ["https"]


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")
    WTF_CSRF_ENABLED = False
    RATELIMIT_ENABLED = False
